"""Pinecone reader."""

from typing import Any, Dict, List, Optional

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class PineconeReader(BaseReader):
    """Pinecone reader.

    Args:
        api_key (str): Pinecone API key.
        environment (str): Pinecone environment.
    """

    def __init__(self, api_key: str, environment: str):
        """Initialize with parameters."""
        import pinecone  # noqa: F401

        self._api_key = api_key
        self._environment = environment
        pinecone.init(api_key=api_key, environment=environment)

    def load_data(
        self,
        index_name: str,
        id_to_text_map: Dict[str, str],
        vector: Optional[List[float]],
        top_k: int,
        separate_documents: bool = True,
        include_values: bool = True,
        **query_kwargs: Any
    ) -> List[DocumentNode]:
        """Load data from Pinecone.

        Args:
            index_name (str): Name of the index.
            id_to_text_map (Dict[str, str]): A map from ID's to text.
            separate_documents (Optional[bool]): Whether to return separate
                documents per retrieved entry. Defaults to True.
            vector (List[float]): Query vector.
            top_k (int): Number of results to return.
            include_values (bool): Whether to include the embedding in the response.
                Defaults to True.
            **query_kwargs: Keyword arguments to pass to the query.
                Arguments are the exact same as those found in
                Pinecone's reference documentation for the
                query method.

        Returns:
            List[DocumentNode]: A list of documents.
        """
        metadata = {
            "index_name": index_name,
            "id_to_text_map": id_to_text_map,
            "vector": vector,
            "top k": top_k,
            "separate_documents": separate_documents,
            "include_values": include_values,
        }

        import pinecone

        index = pinecone.Index(index_name)
        if "include_values" not in query_kwargs:
            query_kwargs["include_values"] = True
        response = index.query(top_k=top_k, vector=vector, **query_kwargs)

        documents = []
        for match in response.matches:
            if match.id not in id_to_text_map:
                raise ValueError("ID not found in id_to_text_map.")
            text = id_to_text_map[match.id]
            embedding = match.values
            if len(embedding) == 0:
                embedding = None
            documents.append(
                DocumentNode(text=text, embedding=embedding, extra_info=metadata)
            )

        if not separate_documents:
            text_list = [doc.get_text() for doc in documents]
            text = "\n\n".join(text_list)
            documents = [DocumentNode(text=text, extra_info=metadata)]

        return documents
