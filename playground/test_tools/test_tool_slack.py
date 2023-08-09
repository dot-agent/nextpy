import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
openagent_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(openagent_dir)


from openagent.tools.basetool import Tool
from openagent.tools.toolkits.slack_toolkit.slack import SlackToolkit
from openagent import compiler
import ssl
from datetime import datetime
import json
import warnings

# Suppress DeprecationWarning
warnings.filterwarnings("ignore", category=DeprecationWarning)

# ssl = SSLContext(ssl.PROTOCOL_TLS)
client_context = ssl.SSLContext()
date = datetime.now()

# print(dateformat)
slack_tool = SlackToolkit(ssl=client_context, earliest_date=date)
slack_tools = slack_tool.get_tools()
print(slack_tools)

# tools = [requests_get_tool,requests_put_tool,requests_delete_tool,requests_patch_tool, requests_post_tool]

# we use GPT-4 here, but you could use gpt-3.5-turbo as well
llm = compiler.llms.OpenAI(model="gpt-3.5-turbo-16k")

def tool_use(query, tools=slack_tools):
    query = json.loads(query)
    return tools[int(query["index"])].run(query["query"])

experts = compiler(template='''
{{#system~}}
You are a helpful Web assistant. You are given a set of tools to use
{{~#each tools}}
{{this}}
{{/each}}
{{~/system}}

{{#user~}}
I want a response to the following question:
{{query}}
Think do you need to use the given tool to answer the question. Provide the answer in either <<Yes>> or <<No>>.
{{~/user}}

{{#assistant~}}
{{gen 'tools_use' temperature=0 max_tokens=300}}
{{~/assistant}}
                        
{{#user~}}
If the answer is Yes then call the tool using the following format '{"index":[index of the tool to be used in the tools list], "query":[query to be passed]'
If the answer is No, answer to the {{query}} itself.
{{~/user}}

{{#assistant~}}
{{gen 'action' temperature=0 max_tokens=500}}
{{#if (tools_use)=="Yes"}}
{{(tool_func action)}}
{{/if}}
{{~/assistant}}    
                        
{{#user~}}
Summarise the answer in one sentence
{{~/user}}
                        
{{#assistant~}}
{{gen 'final_answer' temperature=0 max_tokens=500}}
{{~/assistant}}
''', 
llm=llm, tools = slack_tools, tool_func = tool_use, stream = False)

out = experts(query='Hi')
print(out)

