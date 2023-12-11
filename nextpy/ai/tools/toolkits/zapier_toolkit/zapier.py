"""Notion tool spec."""

from typing import List

from nextpy.ai.tools.basetool import BaseTool
from nextpy.ai.tools.toolkits.base import BaseToolkit
from nextpy.ai.tools.toolkits.notion_toolkit.notion.base import LoadData, SearchData

SEARCH_URL = "https://api.notion.com/v1/search"


class ZapierToolkit(BaseToolkit):
    api_key: str = None
    oauth_access_token: str = None

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            LoadData(api_key=self.api_key, oauth_access_token=self.oauth_access_token),
            SearchData(
                integration_token=self.api_key,
                oauth_access_token=self.oauth_access_token,
            ),
        ]
