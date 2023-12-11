"""Toolkit for interacting with the local filesystem."""
from __future__ import annotations

from typing import List, Optional

from pydantic import root_validator

from nextpy.ai.tools.basetool import BaseTool
from nextpy.ai.tools.toolkits.base import BaseToolkit
from nextpy.ai.tools.toolkits.file_toolkit.file.copy import CopyFileTool
from nextpy.ai.tools.toolkits.file_toolkit.file.delete import DeleteFileTool
from nextpy.ai.tools.toolkits.file_toolkit.file.listdir import ListDirectoryTool
from nextpy.ai.tools.toolkits.file_toolkit.file.move import MoveFileTool
from nextpy.ai.tools.toolkits.file_toolkit.file.read import ReadFileTool
from nextpy.ai.tools.toolkits.file_toolkit.file.search import FileSearchTool
from nextpy.ai.tools.toolkits.file_toolkit.file.write import WriteFileTool

_FILE_TOOLS = {
    tool_cls.__fields__["name"].default: tool_cls
    for tool_cls in [
        CopyFileTool,
        DeleteFileTool,
        FileSearchTool,
        MoveFileTool,
        ReadFileTool,
        WriteFileTool,
        ListDirectoryTool,
    ]
}


class FileManagementToolkit(BaseToolkit):
    """Toolkit for interacting with a Local Files."""

    root_dir: Optional[str] = None
    """If specified, all file operations are made relative to root_dir."""
    selected_tools: Optional[List[str]] = None
    """If provided, only provide the selected tools. Defaults to all."""

    @root_validator
    def validate_tools(cls, values: dict) -> dict:
        selected_tools = values.get("selected_tools") or []
        for tool_name in selected_tools:
            if tool_name not in _FILE_TOOLS:
                raise ValueError(
                    f"File Tool of name {tool_name} not supported."
                    f" Permitted tools: {list(_FILE_TOOLS)}"
                )
        return values

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        allowed_tools = self.selected_tools or _FILE_TOOLS.keys()
        tools: List[BaseTool] = []
        for tool in allowed_tools:
            tool_cls = _FILE_TOOLS[tool]
            tools.append(tool_cls(root_dir=self.root_dir))  # type: ignore
        return tools


__all__ = ["FileManagementToolkit"]
