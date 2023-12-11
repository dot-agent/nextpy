"""Tools for making requests to an API endpoint."""

from typing import List

from nextpy.ai.tools.basetool import BaseTool
from nextpy.ai.tools.toolkits.base import BaseToolkit
from nextpy.ai.tools.toolkits.requests_toolkit.requests.base import (
    RequestsDeleteTool,
    RequestsGetTool,
    RequestsPatchTool,
    RequestsPostTool,
    RequestsPutTool,
)
from nextpy.ai.tools.toolkits.requests_toolkit.requests.utils import TextRequestsWrapper


class RequestsToolkit(BaseToolkit):
    """Base class for requests tools."""

    requests_wrapper: TextRequestsWrapper

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            RequestsGetTool(requests_wrapper=self.requests_wrapper),
            RequestsPostTool(requests_wrapper=self.requests_wrapper),
            RequestsPatchTool(requests_wrapper=self.requests_wrapper),
            RequestsPutTool(requests_wrapper=self.requests_wrapper),
            RequestsDeleteTool(requests_wrapper=self.requests_wrapper),
        ]
