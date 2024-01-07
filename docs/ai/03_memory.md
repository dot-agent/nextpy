
Function extract\_text:

extract\_text(string) - A standalone function that extracts the AI's response text from the prompt engine output. Removes a predefined start and end string from the given input string to extract the actual AI response. Returns the extracted AI response text.

class SimpleMemory(BaseMemory, BaseModel): - Defines the SimpleMemory 

class that inherits from BaseMemory.

Methods

Method add\_memory:

def add\_memory(self, prompt: str, llm\_response: Any) -> None: - Adds a conversation memory to the store.

Parameters:

prompt (str): The user's prompt or input.

llm\_response (Any): The AI's response to the prompt.

Functionality:

This method checks if the given (prompt, llm\_response) pair already exists in memory.

If not, it appends a dictionary containing the prompt and response to the list of self.messages.

Method get\_memory:

def get\_memory(self, \*\*kwargs) -> str: - Retrieves all memories from the store.

Parameters:

kwargs (dict): Additional keyword arguments (not used in this method).

Functionality:

It constructs a formatted string containing all conversations stored in self.messages.

For each conversation, it appends the user's prompt and AI's response to the formatted string.

Returns the formatted string containing all memories.

Method remove\_memory:

def remove\_memory(self, prompt: str) -> None: - Removes a specific memory from the store.

Parameters:

prompt (str): The user's prompt to be removed.

Functionality:

Iterates through each conversation in self.messages. If a conversation's prompt matches the provided prompt, it is removed from the list.

Method clear:

def clear(self) -> None: - Clears all stored memories.

Functionality:

Clears the list of self.messages, effectively removing all stored conversations.

class SummaryMemory(BaseMemory, BaseModel): - Defines the SummaryMemory class that inherits from BaseMemory.

Attributes:

current\_summary (str): Keeps track of the current conversation summary.

messages\_in\_summary (List[Dict[BaseMessage, Any]]): Stores a list of messages that have been included in the summary.

Methods

Method add\_memory:

This method adds a new conversation memory to the store, avoiding duplicates.

Method get\_memory:

It creates an instance of the llms.OpenAI class using the compiler module. It filters out messages that are already included in the current summary. For each new message, it constructs a string with the user prompt and AI response and updates messages\_in\_summary.

It creates a summarizer using the compiler module with the provided template, llm instance, and new lines. The summary is updated with the extracted text from the summarized memory.

The final summarized memory is returned.

Method remove\_memory:

This method removes a specified memory (user prompt) from the store. It removes the memory from messages, updates current\_summary based on the remaining messages, and clears messages\_in\_summary.

Method clear:

Clears all stored memories, the list of messages in the summary, and resets the current summary.

The SummaryMemory class builds upon the concept of storing and managing conversation memories. It adds the capability to create and update summaries of conversations using a summarization process. The class utilizes the compiler module to interact with OpenAI's language model and performs summarization based on a predefined template. It keeps track of which messages are included in the summary to prevent duplication. The SummaryMemory class seems to be designed for a more advanced conversational AI system that can generate summaries of interactions.


class BufferSummaryMemory(BaseMemory, BaseModel): - Defines the BufferSummaryMemory class that inherits from BaseMemory.

Attributes:

current\_summary (str): Tracks the current conversation summary.

current\_buffer (str): Stores recent messages in a buffer.

messages\_in\_summary (List[Dict[BaseMessage, Any]]): Stores messages included in the summary.

messages\_in\_buffer (List[Dict[BaseMessage, Any]]): Stores messages included in the buffer.

Methods

Method add\_memory:

Adds a new conversation memory to the store while avoiding duplicates.

Method get\_memory:

It deals with both the summary and the buffer. Creates an instance of the llms.OpenAI class using the compiler module. Retrieves the memory\_threshold from kwargs or defaults to 1. Separates recent messages into the buffer and older ones into the summary based on the threshold. Constructs the buffer as a string. Generates a summary only for the new additions to the summary and updates the current\_summary. Returns the combined summary and buffer as the summarized memory.

Method remove\_memory:

Removes a specific memory (user prompt) from the store and updates related variables.

Recalculates the buffer and summary based on the remaining messages and threshold, and updates the current\_buffer and current\_summary accordingly.

Method clear:

Clears all stored memories, the lists of messages in the summary and buffer, and resets the current summary and buffer.

The BufferSummaryMemory class extends the functionality of SummaryMemory by introducing a buffer to store recent messages separately from the summary. This design allows the class to manage recent conversations in a buffer and maintain a more concise summary of older interactions. It utilizes a threshold to decide which messages are included in the buffer and which in the summary. The class's methods manage both the buffer and summary, offering a more sophisticated approach to memory management for conversational AI systems that require both a concise summary and recent context.


class InFileMemory(BaseMemory): - Defines the InFileMemory class that inherits from BaseMemory.

Methods

Method add\_memory:

def add\_memory(self, program\_name: str, session\_id: str, prompt: str, llm\_response: str) -> None: - Adds a memory entry to the store for a specific session of an application.

Parameters:

program\_name (str): Name of the application.

session\_id (str): Identifier for the specific session.

prompt (str): User's input prompt.

llm\_response (str): AI's response to the prompt.

Functionality:

Creates a directory for the specific program if it doesn't exist. Writes the given prompt and response as a JSON entry to the session file. 

Method get\_memory:

def get\_memory(self, program\_name: str, session\_id: str, max\_len: int = 2040 \* 1024, limit: int = 1000): - Retrieves memories from a specific session of an application.

Parameters:

program\_name (str): Name of the application.

session\_id (str): Identifier for the specific session.

max\_len (int): Maximum length of data to read (default is 2040 KB).

limit (int): Maximum number of memories to retrieve (default is 1000).

Functionality:

Reads the last max\_len bytes of the session file. Extracts the last limit JSON entries as memories. Returns the retrieved memories.

Method remove\_memory:

def remove\_memory(self, program\_name: str, session\_id: str, prompt: str = ''): - Removes memories from a specific session of an application.

Parameters:

program\_name (str): Name of the application.

session\_id (str): Identifier for the specific session.

prompt (str): If specified, removes only memories with the given prompt.

Functionality:

If prompt is not specified, it removes the entire session file. If prompt is specified, it removes only the memory entries with the specified prompt.

Method clear:

def clear(self, program\_name: str = ''): - Clears all memories of a specific program or all programs.

Parameters:

program\_name (str): Name of the application to clear memories for (optional).

Functionality:

If program\_name is specified, it clears all memories for that program.

If program\_name is not specified, it iterates through all programs and clears their memories.

Helper functions

def read(self, program\_name: str, session\_id: str, n: int, max\_len: int) -> List[Dict]: - Reads and returns specific memories from a session of an application.

Parameters:

program\_name (str): Name of the application.

session\_id (str): Identifier for the specific session.

n (int): Number of memories to retrieve.

max\_len (int): Maximum length of data to read.

Functionality:

Reads the last max\_len bytes of the session file. Extracts the last n JSON entries as memories. Returns the extracted memories.

def sessions(self, program\_name: str) -> List[Dict]: - Retrieves a list of sessions for a specific program.

Parameters:

program\_name (str): Name of the application.

Functionality:

Searches for session files in the program's directory and retrieves information about each session, including the last modified time and latest memory entry.

Method \_memories\_dirs:

A private method that creates the directory for storing memory data if it doesn't exist and returns the directory path.

The InFileMemory class provides a memory management system that saves conversation data in individual session files on the local filesystem. It's designed to persistently store conversations for different applications and sessions. It offers methods to add memories, retrieve memories, remove memories, clear memories, read specific memories, and retrieve session information. This class could be useful for maintaining a history of interactions in a more permanent storage location.

class ReadOnlyMemory(BaseMemory): - Defines the ReadOnlyMemory class that inherits from BaseMemory.

Attributes:

memory: BaseMemory - Holds the reference to the original memory instance.

Constructor:

def \_\_init\_\_(self, memory: BaseMemory): - Initializes the ReadOnlyMemory instance with a provided memory instance.

Parameters:

memory (BaseMemory): The memory instance that this read-only memory will wrap.

Methods

Method add\_memory:

def add\_memory(self, prompt: str, llm\_response: Any) -> None: - Prevents adding memory in a read-only context.

Functionality:

This method is implemented with an empty body, preventing any addition to the underlying memory instance.

Method get\_memory:

def get\_memory(self, \*\*kwargs) -> Any: - Retrieves entire memory from the store.

Parameters:

kwargs (dict): Additional keyword arguments that may be passed to the underlying memory's get\_memory method.

Functionality:

Calls the get\_memory method of the underlying memory instance and returns its result.

Method remove\_memory:

def remove\_memory(self, prompt: str) -> None: - Prevents memory removal in a read-only context.

Functionality:

This method is implemented with an empty body, preventing any removal from the underlying memory instance.

Method clear:

def clear(self) -> None: - Prevents clearing the memory in a read-only context.

Functionality:

This method is implemented with an empty body, preventing any clearing of the underlying memory instance.

Property memory\_keys:

@property def memory\_keys(self) -> List[str]: - Returns a list of prompts for all memories in the underlying memory.

Functionality:

Iterates through each conversation in the underlying memory and retrieves their prompts, creating a list of prompts.

The ReadOnlyMemory class is a memory wrapper that provides a read-only view of an existing memory instance. It prevents modifications to the underlying memory while allowing data retrieval operations like getting all memories and extracting memory keys (prompts). This class is useful in scenarios where you want to ensure that memory data remains unmodified during certain operations or contexts.

Implementation with Compiler

Compiler \_\_init\_\_.py

Initializing a compiler takes an optional parameter ‘memory’, which should be a instance of one of the memory classes explained above. If memory is passed, the compiler passes it to the Program class. Additionally, if the user doesn’t prefer the conversation history to be displayed in the system prompt (in case the user doesn’t want a system prompt or wants to pass it with instructions, etc.), they can add a ConversationHistory variable to the prompt template.

\_program.py

1. Firstly, after all the variables are initialized, the class init function checks if memory has been passed. If yes, it further checks if the prompt template has a ConversationHistory variable, and if there isn’t, the ‘add\_variable’ function, declared in the \_program.py file itself, is called to add it to the prompt template at the end of the system prompt.

1. Next, the value for ConversationHistory is added to the keyword arguments, (kwargs), by getting it from the Memory.get\_memory() function explained above. 

1. The memory variable is then passed to all Program class instances created for further use.

1. After the response has been completely generated, the program again checks if memory exists. If yes, then it calls the extract\_text() function, declared the \_program.py file itself to get the user prompt and llm response key-value pair, which is then passed to Memory.add\_memory() to save it into the memory. 

Implementation with Agent

The usage is same for agent as for the compiler. Simply create a memory instance and pass into the agent constructor. The agent \_\_init\_\_() function passes it into the compiler when the object is created, and the implementation continues as explained above.

Future implementation

Here are some suggestions on what could be improved on memory in the future.

1. Manual saving of memory: Through a parameter, the user can disable the adding of prompt and llm responses by the Program instance, as explained in implementation with compiler, step 4. Instead, the user can call the memory.add\_memory() themselves if they wish to add only certain variables. This can be called either after the compiler/agent is run, or in the prompt 

template as well.

1. Fixing infile memory: Unfortunately, while the infile memory has been created and works, it has not been integrated into the compiler, but it only requires the parameters to be taken from the user and to be passed into the add\_memory function, similar to how the memory\_threshold variable has been passed for BufferSummaryMemory. 
