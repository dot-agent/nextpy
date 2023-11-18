import os
from typing import Optional, Type

from pydantic import BaseModel, Field

from openams.tools.basetool import BaseTool
from openams.tools.toolkits.file_toolkit.file.utils import (
    INVALID_PATH_TEMPLATE,
    BaseFileToolMixin,
    FileValidationError,
)


class FileDeleteInput(BaseModel):
    """Input for DeleteFileTool."""

    file_path: str = Field(..., description="Path of the file to delete")


class DeleteFileTool(BaseFileToolMixin, BaseTool):
    name: str = "file_delete"
    args_schema: Type[BaseModel] = FileDeleteInput
    description: str = "Delete a file"

    def run(
        self,
        file_path: str,
    ) -> str:
        try:
            file_path_ = self.get_relative_path(file_path)
        except FileValidationError:
            return INVALID_PATH_TEMPLATE.format(arg_name="file_path", value=file_path)
        if not file_path_.exists():
            return f"Error: no such file or directory: {file_path}"
        try:
            os.remove(file_path_)
            return f"File deleted successfully: {file_path}."
        except Exception as e:
            return "Error: " + str(e)

    async def _arun(
        self,
        file_path: str,
    ) -> str:
        # TODO: Add aiofiles method
        raise NotImplementedError