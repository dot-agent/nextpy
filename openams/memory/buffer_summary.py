from typing import List, Dict, Any
from pydantic import BaseModel

from openams import compiler
from openams.memory import BaseMemory
from openams.schema import BaseMessage
from .prompt import SUMMARIZER_TEMPLATE

def extract_text(string):
    """function for getting the user prompt and llm response from the compiler output"""
    end_string="<|im_end|>"
    start_string="New summary:<|im_end|>\n\n<|im_start|>assistant\n"
    string = string.replace(start_string, "", 1)
    start_index = string.find(start_string)
    end_index = string.find(end_string, start_index + len(start_string))
    return string[start_index + len(start_string):end_index]


class BufferSummaryMemory(BaseMemory, BaseModel):
    current_summary: str = ""
    current_buffer: str = ""
    messages_in_summary: List[Dict[BaseMessage, Any]] = []
    messages_in_buffer: List[Dict[BaseMessage, Any]] = []

    def add_memory(self, prompt: str, llm_response: Any) -> None:
        """Add a self-created message to the store"""
        unique = True
        for conversation in self.messages:
            if conversation['prompt'] == prompt and conversation['llm_response']  == llm_response:
                unique = False
        if unique:
            self.messages.append({'prompt': prompt, 'llm_response': llm_response})

    def get_memory(self, **kwargs) -> str:
        """Retrieve entire memory from the store."""

        # Create llm instance
        llm = compiler.endpoints.OpenAI(model="gpt-3.5-turbo")
        
        # get variables
        if 'memory_threshold' not in kwargs.keys():
            memory_threshold = 1
        else:
            memory_threshold = kwargs['memory_threshold']

        # get new messages in memory
        new_messages = [item for item in self.messages if item not in self.messages_in_summary and item not in self.messages_in_buffer]

        if len(new_messages) != 0:
            # split conversations for buffer and summary according to threshold         
            buffer_messages = self.messages[-1*memory_threshold:] # buffer
            summary_messages =  [item for item in self.messages if item not in buffer_messages] # summary
            
            # get messages in the buffer format as text
            self.current_buffer = ""
            for conversation in buffer_messages:
                self.current_buffer = self.current_buffer + "Human: " + conversation['prompt'] + "\n" + "AI: " + conversation['llm_response'] + "\n"
            self.messages_in_buffer=buffer_messages

            # get the new messages to be added in the summary
            additions_to_summary = [item for item in summary_messages if item not in self.messages_in_summary]

            if len(additions_to_summary) != 0:
                additions_to_summary_as_text=""
                
                for conversation in additions_to_summary:
                    additions_to_summary_as_text = additions_to_summary_as_text + "Human: " + conversation['prompt'] + "\n" + "AI: " + conversation['llm_response'] + "\n"

                self.messages_in_summary = summary_messages

                summarizer = compiler(template=SUMMARIZER_TEMPLATE, llm=llm, stream = False)
                summarized_memory = summarizer(summary=self.current_summary, new_lines= additions_to_summary_as_text)
                self.current_summary = extract_text(summarized_memory.text)
                
                summarized_memory = "Current conversation:\n"+self.current_summary + "\n" + self.current_buffer
            else:
                summarized_memory= "Current conversation:\n"+self.current_buffer
        
        else:
            if len(self.current_buffer) != 0 or len(self.current_summary) != 0: 
                summarized_memory = "Current conversation:\n"+self.current_summary + "\n" + self.current_buffer
            else:
                summarized_memory = ""
                
        return summarized_memory

    def remove_memory(self, prompt: str, llm: Any, threshold=1) -> None:
        """Remove a memory from the store."""

        # update messages
        for conversation in self.messages:
            if conversation['prompt'] == prompt:
                # updating messages
                self.messages.remove(conversation)
                
                # updating other variables
                self.current_summary = ""
                self.current_buffer = ""
                self.messages_in_buffer.clear()
                self.messages_in_summary.clear()

                # get new messages in memory
                new_messages = [item for item in self.messages if item not in self.messages_in_summary and item not in self.messages_in_buffer]

                if len(new_messages) != 0:
                    # split conversations for buffer and summary according to threshold         
                    buffer_messages = self.messages[-1*threshold:] # buffer
                    summary_messages =  [item for item in self.messages if item not in buffer_messages] # summary
                    
                    # get messages in the buffer format as text
                    self.current_buffer = ""
                    for conversation in buffer_messages:
                        self.current_buffer = self.current_buffer + "Human: " + conversation['prompt'] + "\n" + "AI: " + conversation['llm_response'] + "\n"
                    self.messages_in_buffer=buffer_messages

                    # get the new messages to be added in the summary
                    additions_to_summary = [item for item in summary_messages if item not in self.messages_in_summary]

                    if len(additions_to_summary) != 0:
                        additions_to_summary_as_text=""
                        print(additions_to_summary_as_text)
                        
                        for conversation in additions_to_summary:
                            additions_to_summary_as_text = additions_to_summary_as_text + "Human: " + conversation['prompt'] + "\n" + "AI: " + conversation['llm_response'] + "\n"

                        self.messages_in_summary = summary_messages

                        summarizer = compiler(template=SUMMARIZER_TEMPLATE, llm=llm, stream = False)
                        summarized_memory = summarizer(summary=self.current_summary, new_lines= additions_to_summary_as_text)
                        self.current_summary = extract_text(summarized_memory.text)
                break
    
    def clear(self) -> None:
        """Clear all memories."""
        self.messages.clear()
        self.messages_in_summary.clear()
        self.messages_in_buffer.clear()
        self.current_summary = ""
        self.current_buffer = ""