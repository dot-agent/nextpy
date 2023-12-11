"""Azblob file and directory reader.

A loader that fetches a file or iterates through a directory on Azblob or.

"""

from typing import Dict, List, Optional, Union

from nextpy.ai import download_loader
from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class OpendalAzblobReader(BaseReader):
    """General reader for any Azblob file or directory."""

    def __init__(
        self,
        container: str,
        path: str = "/",
        endpoint: str = "",
        account_name: str = "",
        account_key: str = "",
        file_extractor: Optional[Dict[str, Union[str, BaseReader]]] = None,
    ) -> None:
        """Initialize Azblob container, along with credentials if needed.

        If key is not set, the entire bucket (filtered by prefix) is parsed.

        Args:
        container (str): the name of your azblob bucket
        path (str): the path of the data. If none is provided,
            this loader will iterate through the entire bucket. If path is endswith `/`, this loader will iterate through the entire dir. Otherwise, this loeader will load the file.
        endpoint Optional[str]: the endpoint of the azblob service.
        account_name (Optional[str]): provide azblob access key directly.
        account_key (Optional[str]): provide azblob access key directly.
        file_extractor (Optional[Dict[str, BaseReader]]): A mapping of file
            extension to a BaseReader class that specifies how to convert that file
            to text. See `SimpleDirectoryReader` for more details.

        """
        super().__init__()

        self.path = path
        self.file_extractor = file_extractor

        # opendal service related config.
        self.options = {
            "container": container,
            "endpoint": endpoint,
            "account_name": account_name,
            "account_key": account_key,
        }

    def load_data(self) -> List[DocumentNode]:
        """Load file(s) from OpenDAL."""
        try:
            from nextpy.ai.rag.document_loaders.utils import import_loader

            OpendalReader = import_loader("OpendalReader")
        except ImportError:
            OpendalReader = download_loader("OpendalReader")

        loader = OpendalReader(
            scheme="azblob",
            path=self.path,
            file_extractor=self.file_extractor,
            **self.options,
        )

        return loader.load_data()
