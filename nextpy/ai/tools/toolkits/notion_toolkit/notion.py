# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Notion tool spec."""

from typing import List, Optional

from nextpy.ai.tools.basetool import BaseTool
from nextpy.ai.tools.toolkits.base import BaseToolkit
from nextpy.ai.tools.toolkits.notion_toolkit.notion.base import LoadData, SearchData

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
            LoadData(integration_token=self.integration_token),
            SearchData(integration_token=self.integration_token),
        ]
