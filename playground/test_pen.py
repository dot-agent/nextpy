import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
openagent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(openagent_dir)

from openagent import compiler

import re

# we use GPT-4 here, but you could use gpt-3.5-turbo as well
llm = compiler.llms.OpenAI(model="gpt-3.5-turbo",api_key="OpenAI API Key")


with open("prompt_on_the_outside.🖊️", "r") as f:
       file_content = f.read()
experts = compiler(template='''{{file_content}} hey how are things''', llm=llm, stream = False,log=True)


# execute the program for a specific goal
out = experts(query='How can I be more productive?', file_content=file_content)

print(out())
