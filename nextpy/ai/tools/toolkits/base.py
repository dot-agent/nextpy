"""Toolkits for agents."""
from abc import abstractmethod
from typing import List

from pydantic import BaseModel

from nextpy.ai.tools.basetool import BaseTool


class BaseToolkit(BaseModel):
    """Class responsible for defining a collection of related tools."""

    @abstractmethod
    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
