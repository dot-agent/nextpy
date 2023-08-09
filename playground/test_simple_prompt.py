import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
openagent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(openagent_dir)


from openagent import compiler
import re
from dotenv import load_dotenv
from openagent.memory import SummaryMemory

load_dotenv()

# we use GPT-4 here, but you could use gpt-3.5-turbo as well
llm = compiler.llms.OpenAI(model="gpt-3.5-turbo-16k")
memory = SummaryMemory()


experts = compiler(template='''
{{#system~}}
You are a helpful and terse assistant.
{{~/system}}

{{#user~}}
I want a response to the following question:
{{query}}
Name 3 world-class experts (past or present) who would be great at answering this?
Don't answer the question yet.
{{~/user}}

{{#assistant~}}
{{gen 'expert_names' temperature=0 max_tokens=300}}
{{~/assistant}}

{{#user~}}
Great, now please answer the question as if these experts had collaborated in writing a joint anonymous answer.
{{~/user}}

{{#assistant~}}
{{gen 'answer' temperature=0 max_tokens=500}}
{{~/assistant}}
''', llm=llm, stream = False, memory=memory)


# execute the program for a specific goal
out = experts(query='How can I be more productive?')
print(out)