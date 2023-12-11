"""Deepdoctection Data Reader."""

from pathlib import Path
from typing import Dict, List, Optional, Set

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class DeepDoctectionReader(BaseReader):
    """Deepdoctection reader for pdf's.

    Uses deepdoctection as a library to parse PDF files.

    """

    def __init__(self, attrs_as_metadata: Optional[Set] = None) -> None:
        """Init params."""
        import deepdoctection as dd

        self.analyzer = dd.get_dd_analyzer()
        self.attrs_as_metadata = attrs_as_metadata or set()

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[DocumentNode]:
        """Parse file."""
        df = self.analyzer.analyze(path=str(file))
        df.reset_state()
        doc = iter(df)
        result_docs = []
        for page in doc:
            doc_text = page.text
            extra_info = {
                k: getattr(page, k) for k in self.attrs_as_metadata if hasattr(page, k)
            }
            result_docs.append(DocumentNode(text=doc_text, extra_info=extra_info))
        return result_docs
