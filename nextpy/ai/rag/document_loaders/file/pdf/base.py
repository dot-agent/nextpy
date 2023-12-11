"""Read PDF files."""

from pathlib import Path
from typing import Dict, List, Optional

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class PDFReader(BaseReader):
    """PDF reader."""

    def load_data(
        self, file: Path, extra_info: Optional[Dict] = None
    ) -> List[DocumentNode]:
        """Parse file."""
        import pypdf

        with open(file, "rb") as fp:
            # Create a PDF object
            pdf = pypdf.PdfReader(fp)

            # Get the number of pages in the PDF DocumentNode
            num_pages = len(pdf.pages)

            # Iterate over every page
            docs = []
            for page in range(num_pages):
                # Extract the text from the page
                page_text = pdf.pages[page].extract_text()
                page_label = pdf.page_labels[page]
                metadata = {"page_label": page_label, "file_name": file.name}

                if extra_info is not None:
                    metadata.update(extra_info)

                docs.append(DocumentNode(text=page_text, extra_info=metadata))
            return docs
