"""Simple Reader for Memos"""

from typing import Dict, List
from urllib.parse import urljoin

from openams.rag.document_loaders.basereader import BaseReader
from openams.schema import DocumentNode


class MemosReader(BaseReader):
    """Memos reader.

    Reads content from an Memos.

    """

    def __init__(self, host: str = "https://demo.usememos.com/") -> None:
        """Init params."""

        self._memoUrl = urljoin(host, "api/memo")

    def load_data(self, params: Dict = {}) -> List[DocumentNode]:
        """Load data from RSS feeds.

        Args:
            params (Dict): Filtering parameters.

        Returns:
            List[DocumentNode]: List of documents.

        """
        import requests

        documents = []
        realUrl = self._memoUrl

        if not params:
            realUrl = urljoin(self._memoUrl, "all", False)

        try:
            req = requests.get(realUrl, params)
            res = req.json()
        except:
            raise ValueError("Your Memo URL is not valid")

        if "data" not in res:
            raise ValueError("Invalid Memo response")

        memos = res["data"]
        for memo in memos:
            content = memo["content"]
            metadata = {
                "memoUrl": self._memoUrl,
                "creator": memo["creator"],
                "resource_list": memo["resourceList"],
                id: memo["id"],
            }
            documents.append(DocumentNode(text=content, extra_info=metadata))

        return documents
