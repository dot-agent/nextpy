"""Notion tool spec."""

from openagent.tools.toolkits.base import BaseToolkit
from openagent.tools.toolkits.notion_toolkit.notion.base import LoadData
from openagent.tools.toolkits.notion_toolkit.notion.base import SearchData
from openagent.tools.basetool import BaseTool
from typing import Optional, List

SEARCH_URL = "https://api.notion.com/v1/search"


class ZapierToolkit(BaseToolkit):
    api_key: str = None
    oauth_access_token: str = None

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            LoadData(api_key = self.api_key, oauth_access_token = self.oauth_access_token),
            SearchData(integration_token = self.api_key, oauth_access_token = self.oauth_access_token)
            ]