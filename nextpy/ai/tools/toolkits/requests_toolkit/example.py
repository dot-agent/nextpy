# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from nextpy.ai.tools.toolkits.requests_toolkit.requests.base import (
    RequestsGetTool,
    TextRequestsWrapper,
)

# Instantiate the RequestsGetTool with TextRequestsWrapper as requests_wrapper
get_tool = RequestsGetTool(requests_wrapper=TextRequestsWrapper())

# The URL you want to get data from
url = "https://yaml.org"

# Use the get method
response = get_tool._run(url)

# Output the response
print(response)
