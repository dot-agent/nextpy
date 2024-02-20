# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Simple reader that reads wikipedia."""
from typing import Any, List

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class WikipediaReader(BaseReader):
    """Wikipedia reader.

    Reads a page.

    """

    def load_data(
        self, pages: List[str], lang: str = "en", **load_kwargs: Any
    ) -> List[DocumentNode]:
        """Load data from the input directory.

        Args:
            pages (List[str]): List of pages to read.
            lang  (str): language of wikipedia texts (default English)
        """
        import wikipedia

        results = []
        for page in pages:
            wikipedia.set_lang(lang)
            page_content = wikipedia.page(page, **load_kwargs).content
            results.append(
                DocumentNode(
                    text=page_content, extra_info={"page": page, "language": lang}
                )
            )
        return results
