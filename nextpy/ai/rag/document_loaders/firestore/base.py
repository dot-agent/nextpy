"""Firestore Reader."""

from typing import Any, List, Optional

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class FirestoreReader(BaseReader):
    """Simple Firestore reader.

    Args:
        project_id (str): The Google Cloud Project ID.
        *args (Optional[Any]): Additional arguments.
        **kwargs (Optional[Any]): Additional keyword arguments.

    Returns:
        FirestoreReader: A FirestoreReader object.
    """

    def __init__(
        self,
        project_id: str,
        *args: Optional[Any],
        **kwargs: Optional[Any],
    ) -> None:
        """Initialize with parameters."""
        from google.cloud import firestore

        self.project_id = project_id

        self.db = firestore.Client(project=project_id)

    def load_data(self, collection: str) -> List[DocumentNode]:
        """Load data from a Firestore collection, returning a list of Documents.

        Args:
            collection (str): The name of the Firestore collection to read from.

        Returns:
            List[DocumentNode]: A list of DocumentNode objects.
        """
        metadata = {"project_id": self.project_id, "collection": collection}

        documents = []
        col_ref = self.db.collection(collection)
        for doc in col_ref.stream():
            doc_str = ", ".join([f"{k}: {v}" for k, v in doc.to_dict().items()])
            documents.append(DocumentNode(text=doc_str, extra_info=metadata))
        return documents

    def load_document(self, document_url: str) -> DocumentNode:
        """Load a single DocumentNode from Firestore.

        Args:
            document_url (str): The absolute path to the Firestore DocumentNode to read.

        Returns:
            DocumentNode: A DocumentNode object.
        """
        metadata = {"project_id": self.project_id, "document_url": document_url}

        parts = document_url.split("/")
        if len(parts) % 2 != 0:
            raise ValueError(f"Invalid DocumentNode URL: {document_url}")

        ref = self.db.collection(parts[0])
        for i in range(1, len(parts)):
            ref = ref.collection(parts[i]) if i % 2 == 0 else ref.DocumentNode(parts[i])

        doc = ref.get()
        if not doc.exists:
            raise ValueError(f"No such DocumentNode: {document_url}")
        doc_str = ", ".join([f"{k}: {v}" for k, v in doc.to_dict().items()])
        return DocumentNode(text=doc_str, extra_info=metadata)
