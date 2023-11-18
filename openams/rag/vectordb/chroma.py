import uuid

from openams.schema import Document
from openams.rag.vectordb.base import VectorDB
from typing import Any, Optional, Iterable, List, Dict
from openams.rag.vectordb.embeddings.base import Embeddings
import chromadb
import chromadb.config

class Chroma(VectorDB):
    """Wrapper around ChromaDB embeddings platform.

    To use, you should have the ``chromadb`` python package installed.

    Example:
        .. code-block:: python

                from openams.rag.vectordb import Chroma
                from openams.embeddings.openai import OpenAIEmbeddings

                embeddings = OpenAIEmbeddings()
                vectordb = Chroma("openams_collection", embeddings)
    """
    
    def __init__(
        self,
        collection_name: str = "openams",
        embedding_function: Optional[Embeddings] = None,
        persist_directory: Optional[str] = None,
        client_settings: Optional[chromadb.config.Settings] = None,
        collection_metadata: Optional[Dict] = None,
        client: Optional[chromadb.Client] = None,
    ) -> None:
        """Initialize with Chroma client."""

        try:
            import chromadb
            import chromadb.config
        except ImportError:
            raise ValueError(
                "Could not import chromadb python package. "
                "Please install it with `pip install chromadb`."
            )
        
        if client is not None:
            self._client = client
        else:
            if client_settings:
                self._client_settings = client_settings
            else:
                self._client_settings = chromadb.config.Settings()
                if persist_directory is not None:
                    self._client_settings = chromadb.config.Settings(
                        chroma_db_impl="duckdb+parquet",
                        persist_directory=persist_directory,
                    )
            self._client = chromadb.Client(self._client_settings)

        self._embedding_function = embedding_function
        self._persist_directory = persist_directory
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=self._embedding_function.embed_documents
            if self._embedding_function is not None
            else None,
            metadata=collection_metadata,
        )

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> List[str]:
        
        ids = ids or [str(uuid.uuid1()) for _ in texts]
        embeddings = None
        if self._embedding_function is not None:
            embeddings = self._embedding_function.embed_documents(list(texts))
        self._collection.add(
            metadatas=metadatas, embeddings=embeddings, documents=texts, ids=ids
        )
        return ids

    def similarity_search(
            self,
            query: Optional[str] = None, 
            embedding: Optional[List[float]] = None, 
            top_k: int = 5, 
            **kwargs: Any
            ) -> List[Document]:
        """Return docs most similar to query and respective distance score"""

        if (embedding is None and query is None) or (embedding is not None and query is not None):
            raise ValueError("You must provide either query embeddings or query texts, but not both")

        search_results = []
        if self._embedding_function is None:
            if query is not None:
                results = self._collection.query(
                    query_texts=[query],
                    n_results=top_k,
                    **kwargs,
                )
            else:
                results = self._collection.query(
                    query_embeddings=[embedding],
                    n_results=top_k,
                    **kwargs,
                )
        else:
            if query is not None:
                query_embedding = self._embedding_function.embed_query(text=query)
                results = self._collection.query(
                    query_embeddings=[query_embedding],
                    n_results=top_k,
                    **kwargs,
                )
            else:
                results = self._collection.query(
                    query_embeddings=[embedding],
                    n_results=top_k,
                    **kwargs,
                )

        for result in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            document = Document(page_content=result[0], metadata=result[1] or {})
            search_results.append((document, result[2]))

        return search_results
    
    def delete_collection(self) -> None:
        """Delete the collection."""
        self._client.delete_collection(self._collection.name)

    def get(self, include: Optional[List[str]] = None) -> Dict[str, Any]:
        """Gets the collection.

        Args:
            include (Optional[List[str]]): List of fields to include from db.
                Defaults to None.
        """
        if include is not None:
            return self._collection.get(include=include)
        else:
            return self._collection.get()

    def persist(self) -> None:
        """Persist the collection.

        This can be used to explicitly persist the data to disk.
        It will also be called automatically when the object is destroyed.
        """
        if self._persist_directory is None:
            raise ValueError(
                "You must specify a persist_directory on"
                "creation to persist the collection."
            )
        self._client.persist()
    
    def update_document(self, document_id: str, document: Document) -> None:
        # Update a document in the collection.

        text = document.page_content
        metadata = document.metadata
        if self._embedding_function is None:
            raise ValueError(
                "For update, you must specify an embedding function on creation."
            )
        embeddings = self._embedding_function.get_document_embedding([text])

        self._collection.update(
            ids=[document_id],
            embeddings=embeddings,
            documents=[text],
            metadatas=[metadata],
        )

    @classmethod
    def from_texts(
        cls,
        texts: List[str],
        embedding_function: Optional[Embeddings] = None,
        metadatas: Optional[List[dict]] = None,
        ids: Optional[List[str]] = None,
        collection_name: str = "openams",
        persist_directory: Optional[str] = None,
        client_settings: Optional[chromadb.config.Settings] = None,
        client: Optional[chromadb.Client] = None,
        **kwargs: Any,
    ):
        """Create a Chroma vectordb from a raw documents.

        If a persist_directory is specified, the collection will be persisted there.
        Otherwise, the data will be ephemeral in-memory.

        Args:
            texts (List[str]): List of texts to add to the collection.
            collection_name (str): Name of the collection to create.
            persist_directory (Optional[str]): Directory to persist the collection.
            embedding (Optional[Embeddings]): Embedding function. Defaults to None.
            metadatas (Optional[List[dict]]): List of metadatas. Defaults to None.
            ids (Optional[List[str]]): List of document IDs. Defaults to None.
            client_settings (Optional[chromadb.config.Settings]): Chroma client settings

        Returns:
            Chroma: Chroma vectordb.
        """
        chroma_collection = cls(
            collection_name=collection_name,
            embedding_function=embedding_function,
            persist_directory=persist_directory,
            client_settings=client_settings,
            client=client,
        )
        chroma_collection.add_texts(texts=texts, metadatas=metadatas, ids=ids)
        return chroma_collection


    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        embedding_function: Optional[Embeddings] = None,
        ids: Optional[List[str]] = None,
        collection_name: str = "openams",
        persist_directory: Optional[str] = None,
        client_settings: Optional[chromadb.config.Settings] = None,
        client: Optional[chromadb.Client] = None,  # Add this line
        **kwargs: Any,
    ):
        """Create a Chroma vectordb from a list of documents.

        If a persist_directory is specified, the collection will be persisted there.
        Otherwise, the data will be ephemeral in-memory.

        Args:
            collection_name (str): Name of the collection to create.
            persist_directory (Optional[str]): Directory to persist the collection.
            ids (Optional[List[str]]): List of document IDs. Defaults to None.
            documents (List[Document]): List of documents to add to the vectordb.
            embedding (Optional[Embeddings]): Embedding function. Defaults to None.
            client_settings (Optional[chromadb.config.Settings]): Chroma client settings
        Returns:
            Chroma: Chroma vectordb.
        """
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        return cls.from_texts(
            texts=texts,
            embedding=embedding_function,
            metadatas=metadatas,
            ids=ids,
            collection_name=collection_name,
            persist_directory=persist_directory,
            client_settings=client_settings,
            client=client,
            **kwargs
        )