import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
openagent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(openagent_dir)


import chainlit as cl
import openagent.compiler as compiler
from openagent.compiler._program import Log
from openagent import memory
from dotenv import load_dotenv
load_dotenv()

@cl.on_chat_start
def start_chat():
    compiler.llm = compiler.llms.OpenAI(model="gpt-3.5-turbo")


class ChainlitLog(Log):
    def append(self, entry):
        super().append(entry)
        print(entry)
        is_end = entry["type"] == "end"
        is_assistant = entry["name"] == "assistant"
        if is_end and is_assistant:
            cl.run_sync(cl.Message(content=entry["new_prefix"]).send())


memory1 = memory.SimpleMemory()

@cl.on_message
async def main(message: str):
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
        {{~/geneach}}""", memory = memory1
    )

    program(user_text=message, log=ChainlitLog())
