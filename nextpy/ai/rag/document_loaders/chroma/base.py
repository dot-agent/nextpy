"""Chroma Reader."""

from typing import Any

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class ChromaReader(BaseReader):
    """Chroma reader.

    Retrieve documents from existing persisted Chroma collections.

    Args:
        collection_name: Name of the peristed collection.
        persist_directory: Directory where the collection is persisted.

    """

    def __init__(
        self,
        collection_name: str,
        persist_directory: str,
    ) -> None:
        """Initialize with parameters."""
        import chromadb  # noqa: F401
        from chromadb.config import Settings

        self.collection_name = collection_name

        if (collection_name is None) or (persist_directory is None):
            raise ValueError("Please provide a collection name and persist directory.")

        self._client = chromadb.Client(
            Settings(is_persistent=True, persist_directory=persist_directory)
        )
        self._collection = self._client.get_collection(collection_name)

    def load_data(
        self,
        query_vector: Any,
        limit: int = 10,
    ) -> Any:
        """Load data from Chroma.

        Args:
            query_vector (Any): Query
            limit (int): Number of results to return.

        Returns:
            List[DocumentNode]: A list of documents.
        """
        results = self._collection.query(query_embeddings=query_vector, n_results=limit)

        metadata = {
            "collection_name": self.collection_name,
            "query_vector": query_vector,
            "limit": limit,
        }
        documents = []
        for result in zip(results["ids"], results["documents"], results["embeddings"]):
            doc = DocumentNode(
                doc_id=result[0][0],
                text=result[1][0],
                embedding=result[2][0],
                extra_info=metadata,
            )
            documents.append(doc)

        return documents
