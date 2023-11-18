from openams.tools.toolkits.requests_toolkit.requests.base import RequestsGetTool, TextRequestsWrapper

# Instantiate the RequestsGetTool with TextRequestsWrapper as requests_wrapper
get_tool = RequestsGetTool(requests_wrapper=TextRequestsWrapper())

# The URL you want to get data from
url = "https://yaml.org"

# Use the get method
response = get_tool._run(url)

# Output the response
print(response)