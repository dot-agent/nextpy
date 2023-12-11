"""Base reader class."""
from abc import abstractmethod
from typing import Any, List

from nextpy.ai.schema import DocumentNode


class BaseReader:
    """Utilities for loading data from a directory."""

    @abstractmethod
    def load_data(self, *args: Any, **load_kwargs: Any) -> List[DocumentNode]:
        """Load data from the input directory."""

    def load_langchain_documents(self, **load_kwargs: Any) -> List[DocumentNode]:
        """Load data in LangChain DocumentNode format."""
        docs = self.load_data(**load_kwargs)
        return [d.to_langchain_format() for d in docs]
