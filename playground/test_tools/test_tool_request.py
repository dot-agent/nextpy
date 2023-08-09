import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
openagent_dir = os.path.abspath(os.path.join(script_dir, "..", ".."))
sys.path.append(openagent_dir)


from openagent.tools.basetool import Tool
from openagent.tools.toolkits.requests_toolkit.request import RequestsToolkit
from openagent.tools.toolkits.requests_toolkit.requests.base import RequestsGetTool, RequestsPostTool, RequestsPatchTool, RequestsPutTool, RequestsDeleteTool
from openagent.tools.toolkits.requests_toolkit.requests.utils import TextRequestsWrapper
from openagent import compiler
import json

# requests_get_tool = RequestsGetTool(requests_wrapper=TextRequestsWrapper())
# requests_put_tool = RequestsPutTool(requests_wrapper=TextRequestsWrapper())
# requests_post_tool = RequestsPostTool(requests_wrapper=TextRequestsWrapper())
# requests_delete_tool = RequestsDeleteTool(requests_wrapper=TextRequestsWrapper())
# requests_patch_tool = RequestsPatchTool(requests_wrapper=TextRequestsWrapper())


request_tool = RequestsToolkit(requests_wrapper=TextRequestsWrapper())
request_tools = request_tool.get_tools()
# print(request_tools)

# requests_get_tool = Tool(
#     name = "Request_get",
#     func= requests_get_tool.run,
#     description="Useful when you have to get content from a URL"
# )

# requests_put_tool = Tool(
#     name = "Request_put",
#     func= requests_put_tool.run,
#     description = """Use this when you want to PUT to a website.
#     Input should be a json string with two keys: "url" and "data".
#     The value of "url" should be a string, and the value of "data" should be a dictionary of 
#     key-value pairs you want to PUT to the url.
#     Be careful to always use double quotes for strings in the json string.
#     The output will be the text response of the PUT request.
#     """
# )

# requests_delete_tool = Tool(
#     name = "Request_delete",
#     func= requests_delete_tool.run,
#     description="Useful when you have to make delete request to a URL"
# )

# requests_patch_tool = Tool(
#     name = "Request_patch",
#     func= requests_patch_tool.run,
#     description="""Use this when you want to PATCH to a website.
#     Input should be a json string with two keys: "url" and "data".
#     The value of "url" should be a string, and the value of "data" should be a dictionary of 
#     key-value pairs you want to PATCH to the url.
#     Be careful to always use double quotes for strings in the json string
#     The output will be the text response of the PATCH request.
#     """
# )

# requests_post_tool = Tool(
#     name = "Request_post",
#     func= requests_post_tool.run,
#     description="""Use this when you want to POST to a website.
#     Input should be a json string with two keys: "url" and "data".
#     The value of "url" should be a string, and the value of "data" should be a dictionary of 
#     key-value pairs you want to POST to the url.
#     Be careful to always use double quotes for strings in the json string
#     The output will be the text response of the POST request.
#     """
# )

# tools = [requests_get_tool,requests_put_tool,requests_delete_tool,requests_patch_tool, requests_post_tool]

# we use GPT-4 here, but you could use gpt-3.5-turbo as well
llm = compiler.llms.OpenAI(model="gpt-3.5-turbo-16k")

def tool_use(query, tools=request_tools):
    query = json.loads(query)
    return tools[int(query["index"])]._run(query["query"])

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
llm=llm, tools = request_tools, tool_func = tool_use, stream = False)

# get request (Gets the response provided by the given URL)
out = experts(query='Get the content from the following URL : "https://yaml.org"')
print(out)

#All the below tools result in "405 bad gateway, Not Allowed" response
#delete request
# out = experts(query='Make a DELETE request to the following URL : "https://yaml.org"')
# print(out)

# put request
# out = experts(query="""Put to the following URL with the following data {
#   "url": "http://yaml.org",
#   "data": {
#     "key1": "value1",
#     "key2": "value2",
#     "key3": "value3"
#   }
# }""")
# print(out)

# Post request
# out = experts(query="""Post to the following URL with the following data {
#   "url": "http://yaml.org",
#   "data": {
#     "key1": "value1",
#     "key2": "value2",
#     "key3": "value3"
#   }
# }""")
# print(out)

# Patch request
# out = experts(query="""Patch to the following URL with the following data {
#   "url": "http://yaml.org",
#   "data": {
#     "key1": "value1",
#     "key2": "value2",
#     "key3": "value3"
#   }
# }""")
# print(out)
