"""Faiss reader."""

from typing import Any, Dict, List

import numpy as np
from openams.rag.document_loaders.basereader import BaseReader
from openams.schema import DocumentNode


class FaissReader(BaseReader):
    """Faiss reader.

    Retrieves documents through an existing in-memory Faiss index.
    These documents can then be used in a downstream LlamaIndex data structure.
    If you wish use Faiss itself as an index to to organize documents,
    insert documents, and perform queries on them, please use GPTFaissIndex.

    Args:
        faiss_index (faiss.Index): A Faiss Index object (required)

    """

    def __init__(self, index: Any):
        """Initialize with parameters."""
        self._index = index

    def load_data(
        self,
        query: np.ndarray,
        id_to_text_map: Dict[str, str],
        k: int = 4,
        separate_documents: bool = True,
    ) -> List[DocumentNode]:
        """Load data from Faiss.

        Args:
            query (np.ndarray): A 2D numpy array of query vectors.
            id_to_text_map (Dict[str, str]): A map from ID's to text.
            k (int): Number of nearest neighbors to retrieve. Defaults to 4.
            separate_documents (Optional[bool]): Whether to return separate
                documents. Defaults to True.
        Returns:
            List[DocumentNode]: A list of documents.

        """

        metadata = {
            "index": self._index,
            "query": query,
            "id_to_text_map": id_to_text_map,
            "k": k,
            "separate_documents": separate_documents
        }

        dists, indices = self._index.search(query, k)
        documents = []
        for qidx in range(indices.shape[0]):
            for didx in range(indices.shape[1]):
                doc_id = indices[qidx, didx]
                if doc_id not in id_to_text_map:
                    raise ValueError(
                        f"DocumentNode ID {doc_id} not found in id_to_text_map."
                    )
                text = id_to_text_map[doc_id]
                documents.append(DocumentNode(text=text, extra_info=metadata))

        if not separate_documents:
            # join all documents into one
            text_list = [doc.get_text() for doc in documents]
            text = "\n\n".join(text_list)
            documents = [DocumentNode(text=text, extra_info=metadata)]

        return documents
