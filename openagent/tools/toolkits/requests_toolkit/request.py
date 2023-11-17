"""Tools for making requests to an API endpoint."""

from pydantic import BaseModel
from typing import List

from openagent.tools.toolkits.requests_toolkit.requests.utils import TextRequestsWrapper
from openagent.tools.basetool import BaseTool
from openagent.tools.toolkits.base import BaseToolkit
from openagent.tools.toolkits.requests_toolkit.requests.base import RequestsGetTool, RequestsPostTool, RequestsPatchTool, RequestsPutTool, RequestsDeleteTool


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