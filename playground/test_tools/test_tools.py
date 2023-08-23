import sys
import os
from dotenv import load_dotenv

load_dotenv()

script_dir = os.path.dirname(os.path.abspath(__file__))
openagent_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(openagent_dir)

from openagent import compiler
from openagent.llms._openai import OpenAI
from openagent.helpers.youtubeSearch import YouTubeSearchTool
from openagent.helpers.youtubeTranscript import YoutubeTranscriptReader

import json

tools = [YouTubeSearchTool(), YoutubeTranscriptReader()]

llm = OpenAI(model="gpt-3.5-turbo-16k")

temp = '''
{{#system~}}
You are a web assistant who has access to youtube based tool
you have access to the following tools:-
{{tool}}
{{~#each tool}}
{{this}}
{{/each}}
{{~/system}}

{{#user~}}
answer this question - {{query}} by following this steps
first think whether you need to use the tool or not. answer this in one word either <<Yes>> or <<No>>.
{{~/user}}

{{#assistant~}}
{{gen 'tool_use'}}
{{~/assistant}}

{{#user~}}
If the answer is Yes then call the tool using the following format '{"index":[index of the tool to be used in the tools list], "query":[query to be passed]'
If the answer is No, answer to the {{query}} itself.
{{~/user}}

{{#assistant~}}
{{gen 'action' temperature=0 max_tokens=500}}
{{#if (tool_use)=="Yes"}}
{{(tool_func action)}}
{{/if}}
{{~/assistant}}
'''

def tool_use(var:dict, tools=tools):
    var = json.loads(var)
    print(tools[int(var['index'])])
    return tools[int(var['index'])].run(var['query'])

prompt = compiler(template=temp, llm=llm,  tool=tools, tool_func = tool_use, stream=False)

print(prompt(query='give video links for Amitabh Bachan'))