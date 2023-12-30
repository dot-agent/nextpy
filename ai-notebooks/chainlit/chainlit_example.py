# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

# Import necessary modules and libraries
import chainlit as ui
import dotagent.compiler as compiler
from dotagent import memory
from dotagent.compiler._program import Log
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Event handler for the start of a chat using the chainlit UI
@ui.on_chat_start
def start_chat():
    """Initializes the chat by setting the model for the OpenAI compiler to use."""
    compiler.llm = compiler.llms.OpenAI(model="gpt-3.5-turbo")


class ChatLog(Log):
    """Custom logging class to handle chat logs. Extends the default Log class
    and provides additional functionality to handle chat entry appends.
    """

    def append(self, entry):
        """Append a new entry to the chat log and handle special events.
        

        Parameters:
        - entry (dict): The chat entry to append.
        """
        # Call the parent class's append method
        super().append(entry)
        
        # Print the chat entry to the console
        print(entry)
        
        # Check for specific chat entry conditions
        is_end = entry["type"] == "end"
        is_assistant = entry["name"] == "assistant"
        
        # If the chat entry marks the end of the assistant's message, 
        # trigger a synchronous UI message event
        if is_end and is_assistant:
            ui.run_sync(ui.Message(content=entry["new_prefix"]).send())


# Initialize a simple memory module for the chat application
memory = memory.SimpleMemory()

# Event handler for incoming messages using the chainlit UI
@ui.on_message
async def main(message: str):
    """Main chat handler. Compiles the specified chat program and processes
    the incoming user message.
    

    Parameters:
    - message (str): The incoming user message.
    """
    # Define the chat program using the OpenAI compiler DSL
    program = compiler(
        """
        {{#system~}}
        You are a helpful assistant
        {{~/system}}

        {{~#geneach 'conversation' stop=False}}
        {{#user~}}
        {{set 'this.user_text' (await 'user_text')  hidden=False}}
        {{~/user}}

        {{#assistant~}}
        {{gen 'this.ai_text' temperature=0 max_tokens=300}}
        {{~/assistant}}
        {{~/geneach}}""", memory=memory
    )

    # Execute the chat program with the provided user message and log handler
    program(user_text=message, log=ChatLog())
