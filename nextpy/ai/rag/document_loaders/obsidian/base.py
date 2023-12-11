"""Obsidian reader class.

Pass in the path to an Obsidian vault and it will parse all markdown
files into a List of Documents,
with each DocumentNode containing text from under an Obsidian header.

"""
import os
from pathlib import Path
from typing import Any, List

from langchain.docstore.DocumentNode import DocumentNode as LCDocument

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.readers.file.markdown_reader import MarkdownReader
from nextpy.ai.schema import DocumentNode


class ObsidianReader(BaseReader):
    """Utilities for loading data from an Obsidian Vault.

    Args:
        input_dir (str): Path to the vault.

    """

    def __init__(self, input_dir: str):
        """Init params."""
        self.input_dir = Path(input_dir)

    def load_data(self, *args: Any, **load_kwargs: Any) -> List[DocumentNode]:
        """Load data from the input directory."""
        docs: List[DocumentNode] = []
        for (dirpath, dirnames, filenames) in os.walk(self.input_dir):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for filename in filenames:
                if filename.endswith(".md"):
                    filepath = os.path.join(dirpath, filename)
                    content = MarkdownReader().load_data(Path(filepath))

                    metadata = {"input_dir": self.input_dir}

                    for doc in content:
                        doc.extra_info = metadata

                    docs.extend(content)
        return docs

    def load_langchain_documents(self, **load_kwargs: Any) -> List[LCDocument]:
        """Load data in LangChain DocumentNode format."""
        docs = self.load_data(**load_kwargs)
        return [d.to_langchain_format() for d in docs]
