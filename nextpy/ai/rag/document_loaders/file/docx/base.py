# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Read Microsoft Word files."""

from pathlib import Path
from typing import Dict, List, Optional

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class DocxReader(BaseReader):
    """Docx Reader."""

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[DocumentNode]:
        """Parse file."""
        import docx2txt

        text = docx2txt.process(file)
        metadata = {"file_name": file.name}

        if extra_info is not None:
            metadata.update(extra_info)

        return [DocumentNode(text=text, extra_info=metadata)]
