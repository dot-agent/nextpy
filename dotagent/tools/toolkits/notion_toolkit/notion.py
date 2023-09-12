"""Notion tool spec."""

from dotagent.tools.toolkits.base import BaseToolkit
from dotagent.tools.toolkits.notion_toolkit.notion.base import LoadData, SearchData
from dotagent.tools.basetool import BaseTool
from typing import Optional, List

SEARCH_URL = "https://api.notion.com/v1/search"


class NotionToolkit(BaseToolkit):
    """Notion tool spec.

    Currently a simple wrapper around the data loader.
    TODO: add more methods to the Notion spec.

    """
    integration_token: Optional[str] = None

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            LoadData(integration_token = self.integration_token),
            SearchData(integration_token = self.integration_token)
        ]