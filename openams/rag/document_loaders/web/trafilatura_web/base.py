from typing import List

from openams.rag.document_loaders.basereader import BaseReader
from openams.schema import DocumentNode


class TrafilaturaWebReader(BaseReader):
    """Trafilatura web page reader.

    Reads pages from the web.
    Requires the `trafilatura` package.

    """

    def load_data(self, urls: List[str]) -> List[DocumentNode]:
        """Load data from the urls.

        Args:
            urls (List[str]): List of URLs to scrape.

        Returns:
            List[DocumentNode]: List of documents.

        """
        import trafilatura

        if not isinstance(urls, list):
            raise ValueError("urls must be a list of strings.")
        documents = []
        for url in urls:
            downloaded = trafilatura.fetch_url(url)
            response = trafilatura.extract(downloaded)
            metadata = {"url": url}
            documents.append(DocumentNode(text=response, extra_info=metadata))

        return documents
