import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
openagent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(openagent_dir)

from openagent import compiler
from openagent import memory

import re
from dotenv import load_dotenv
load_dotenv()

# we use GPT-4 here, but you could use gpt-3.5-turbo as well
llm = compiler.llms.OpenAI(model="gpt-3.5-turbo-16k")

memory1 = memory.SummaryMemory()

experts = compiler(template='''
{{#system~}}
You are a helpful and terse assistant.
{{~/system}}

{{#user~}}
{{ query }}
{{~/user}}

{{#assistant~}}
{{gen 'result' temperature=0 max_tokens=300}}
{{~/assistant}}
''', llm=llm, stream = False, memory=memory1, memory_threshold = 1)


query='How can I be more productive?'
out = experts(query=query)

query2='Can you give me more suggestions?'
out2 = experts(query=query2)

query3='What should I avoid to achieve my goal?'
out3= experts(query=query3)

query4='Create a action plan for me to increase my productivity.'
out4= experts(query=query4)

query5='Suggest me books to read on productivity.'
out5= experts(query=query5)

memory1.clear()
memory1.messages

memory1.messages_in_summary


