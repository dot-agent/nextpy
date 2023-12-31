# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import os
from typing import Type

from pydantic import BaseModel, Field

from nextpy.ai.tools.basetool import BaseTool
from nextpy.ai.tools.toolkits.file_toolkit.file.utils import (
    INVALID_PATH_TEMPLATE,
    BaseFileToolMixin,
    FileValidationError,
)


class DirectoryListingInput(BaseModel):
    """Input for ListDirectoryTool."""

    dir_path: str = Field(default=".", description="Subdirectory to list.")


class ListDirectoryTool(BaseFileToolMixin, BaseTool):
    name: str = "list_directory"
    args_schema: Type[BaseModel] = DirectoryListingInput
    description: str = "List files and directories in a specified folder"

    def run(
        self,
        dir_path: str = ".",
    ) -> str:
        try:
            dir_path_ = self.get_relative_path(dir_path)
        except FileValidationError:
            return INVALID_PATH_TEMPLATE.format(arg_name="dir_path", value=dir_path)
        try:
            entries = os.listdir(dir_path_)
            if entries:
                return "\n".join(entries)
            else:
                return f"No files found in directory {dir_path}"
        except Exception as e:
            return "Error: " + str(e)

    async def _arun(
        self,
        dir_path: str,
    ) -> str:
        # TODO: Add aiofiles method
        raise NotImplementedError
