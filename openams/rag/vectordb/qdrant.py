"""Wrapper around Qdrant vector database."""
from __future__ import annotations

import uuid
import warnings
from itertools import islice
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
)

import numpy as np

from openams.schema import Document
from openams.rag.vectordb.embeddings.base import Embeddings
from openams.rag.vectordb import VectorDB

if TYPE_CHECKING:
    from qdrant_client.conversions import common_types
    from qdrant_client.http import models as rest

    DictFilter = Dict[str, Union[str, int, bool, dict, list]]
    MetadataFilter = Union[DictFilter, common_types.Filter]


class Qdrant(VectorDB):
    """Wrapper around Qdrant vector database.

    To use you should have the ``qdrant-client`` package installed.

    Example:
        .. code-block:: python

            from qdrant_client import QdrantClient
            from openams.rag.vectordb import Qdrant

            client = QdrantClient()
            collection_name = "MyCollection"
            qdrant = Qdrant(client, collection_name, embedding_function)
    """

    CONTENT_KEY = "page_content"
    METADATA_KEY = "metadata"

    def __init__(
        self,
        client: Any,
        collection_name: str,
        embedding_function: Optional[Callable] = None,
        content_payload_key: str = CONTENT_KEY,
        metadata_payload_key: str = METADATA_KEY,
    ):
        """Initialize with necessary components."""
        try:
            import qdrant_client
        except ImportError:
            raise ValueError(
                "Could not import qdrant-client python package. "
                "Please install it with `pip install qdrant-client`."
            )

        if not isinstance(client, qdrant_client.QdrantClient):
            raise ValueError(
                f"client should be an instance of qdrant_client.QdrantClient, "
                f"got {type(client)}"
            )

        self._embeddings_function = embedding_function
        self.client: qdrant_client.QdrantClient = client
        self.collection_name = collection_name
        self.content_payload_key = content_payload_key or self.CONTENT_KEY
        self.metadata_payload_key = metadata_payload_key or self.METADATA_KEY

        if embedding_function is not None:
            warnings.warn(
                "Using `embedding_function` is deprecated. "
                "Pass `Embeddings` instance to `embeddings` instead."
            )

        if not isinstance(embedding_function, Embeddings):
            warnings.warn(
                "`embeddings` should be an instance of `Embeddings`."
                "Using `embeddings` as `embedding_function` which is deprecated"
            )
            self._embeddings_function = embedding_function
            self.embeddings = None

    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[List[dict]] = None,
        ids: Optional[Sequence[str]] = None,
        batch_size: int = 64,
        **kwargs: Any,
    ) -> List[str]:
        """Run more texts through the embeddings and add to the vectordb.

        Args:
            texts: Iterable of strings to add to the vectordb.
            metadatas: Optional list of metadatas associated with the texts.
            ids:
                Optional list of ids to associate with the texts. Ids have to be
                uuid-like strings.
            batch_size:
                How many vectors upload per-request.
                Default: 64

        Returns:
            List of ids from adding the texts into the vectordb.
        """
        from qdrant_client.http import models as rest

        added_ids = []
        texts_iterator = iter(texts)
        metadatas_iterator = iter(metadatas or [])
        ids_iterator = iter(ids or [uuid.uuid4().hex for _ in iter(texts)])
        while batch_texts := list(islice(texts_iterator, batch_size)):
            # Take the corresponding metadata and id for each text in a batch
            batch_metadatas = list(islice(metadatas_iterator, batch_size)) or None
            batch_ids = list(islice(ids_iterator, batch_size))

            self.client.upsert(
                collection_name=self.collection_name,
                points=rest.Batch.construct(
                    ids=batch_ids,
                    vectors=self._embed_texts(batch_texts),
                    payloads=self._build_payloads(
                        batch_texts,
                        batch_metadatas,
                        self.content_payload_key,
                        self.metadata_payload_key,
                    ),
                ),
            )

            added_ids.extend(batch_ids)

        return added_ids
    


    def similarity_search(
        self,
        query: Optional[str],
        embedding: Optional[List[float]],
        k: int = 4,
        filter: Optional[MetadataFilter] = None,
        search_params: Optional[common_types.SearchParams] = None,
        offset: int = 0,
        score_threshold: Optional[float] = None,
        consistency: Optional[common_types.ReadConsistency] = None,
        **kwargs: Any,
    ) -> List[Document]:
        """Return docs most similar to query.

        Args:
            query: Text to look up documents similar to.
            k: Number of Documents to return. Defaults to 4.
            filter: Filter by metadata. Defaults to None.
            search_params: Additional search params
            offset:
                Offset of the first result to return.
                May be used to paginate results.
                Note: large offset values may cause performance issues.
            score_threshold:
                Define a minimal score threshold for the result.
                If defined, less similar results will not be returned.
                Score of the returned result might be higher or smaller than the
                threshold depending on the Distance function used.
                E.g. for cosine similarity only higher scores will be returned.
            consistency:
                Read consistency of the search. Defines how many replicas should be
                queried before returning the result.
                Values:
                - int - number of replicas to query, values should present in all
                        queried replicas
                - 'majority' - query all replicas, but return values present in the
                               majority of replicas
                - 'quorum' - query the majority of replicas, return values present in
                             all of them
                - 'all' - query all replicas, and return values present in all replicas

        Returns:
            List of Documents most similar to the query.
        """
        if (embedding is None and query is None) or (embedding is not None and query is not None):
            raise ValueError("You must provide either query embeddings or query texts, but not both")
        

        if filter is not None and isinstance(filter, dict):
            warnings.warn(
                "Using dict as a `filter` is deprecated. Please use qdrant-client "
                "filters directly: "
                "https://qdrant.tech/documentation/concepts/filtering/",
                DeprecationWarning,
            )
            qdrant_filter = self._qdrant_filter_from_dict(filter)
        else:
            qdrant_filter = filter
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=embedding,
            query_filter=qdrant_filter,
            search_params=search_params,
            limit=k,
            offset=offset,
            with_payload=True,
            with_vectors=False,  # openams does not expect vectors to be returned
            score_threshold=score_threshold,
            consistency=consistency,
            **kwargs,
        )
        return [
            (
                self._document_from_scored_point(
                    result, self.content_payload_key, self.metadata_payload_key
                ),
                result.score,
            )
            for result in results
        ]
    


    @classmethod
    def from_texts(
        cls: Type[Qdrant],
        texts: List[str],
        embedding_function: Embeddings,
        metadatas: Optional[List[dict]] = None,
        ids: Optional[Sequence[str]] = None,
        location: Optional[str] = None,
        batch_size: Optional[int] = 64,
        **kwargs: Any,
    ) -> Qdrant:
        """Construct Qdrant wrapper from a list of texts.

        Args:
            texts: A list of texts to be indexed in Qdrant.
            embedding: A subclass of `Embeddings`, responsible for text vectorization.
            metadatas:
                An optional list of metadata. If provided it has to be of the same
                length as a list of texts.
            ids:
                Optional list of ids to associate with the texts. Ids have to be
                uuid-like strings.
            location:
                If `:memory:` - use in-memory Qdrant instance.
                If `str` - use it as a `url` parameter.
                If `None` - fallback to relying on `host` and `port` parameters.
            **kwargs:
                Additional arguments passed directly into REST client initialization

        This is a user-friendly interface that:
        1. Creates embeddings, one for each text
        2. Initializes the Qdrant database as an in-memory docstore by default
           (and overridable to a remote docstore)
        3. Adds the text embeddings to the Qdrant database

        This is intended to be a quick way to get started.

        Example:
            .. code-block:: python

                from openams.rag.vectordb import Qdrant
                from openams.embeddings import OpenAIEmbeddings
                embeddings = OpenAIEmbeddings()
                qdrant = Qdrant.from_texts(texts, embeddings, "localhost")
        """
        try:
            import qdrant_client
        except ImportError:
            raise ValueError(
                "Could not import qdrant-client python package. "
                "Please install it with `pip install qdrant-client`."
            )

        from qdrant_client.http import models as rest

        # Just do a single quick embedding to get vector size
        partial_embeddings = embedding_function.embed_documents(texts[:1])
        vector_size = len(partial_embeddings[0])

        collection_name = collection_name or uuid.uuid4().hex
        distance_func = distance_func.upper()

        client = qdrant_client.QdrantClient(
            location=location,
            **kwargs,
        )

        client.recreate_collection(
            collection_name=collection_name,
            vectors_config=rest.VectorParams(
                size=vector_size,
                distance=rest.Distance[distance_func],
            ),
            timeout=timeout,  # type: ignore[arg-type]
        )

        texts_iterator = iter(texts)
        metadatas_iterator = iter(metadatas or [])
        ids_iterator = iter(ids or [uuid.uuid4().hex for _ in iter(texts)])
        while batch_texts := list(islice(texts_iterator, batch_size)):
            # Take the corresponding metadata and id for each text in a batch
            batch_metadatas = list(islice(metadatas_iterator, batch_size)) or None
            batch_ids = list(islice(ids_iterator, batch_size))

            # Generate the embeddings for all the texts in a batch
            batch_embeddings = embedding_function.embed_documents(batch_texts)

            client.upsert(
                collection_name=collection_name,
                points=rest.Batch.construct(
                    ids=batch_ids,
                    vectors=batch_embeddings,
                    payloads=cls._build_payloads(
                        batch_texts,
                        batch_metadatas,
                    ),
                ),
            )

        return cls(
            client=client,
            collection_name=collection_name,
            embedding_function=embedding_function,
        )

    @classmethod
    def _build_payloads(
        cls,
        texts: Iterable[str],
        metadatas: Optional[List[dict]],
        content_payload_key: str,
        metadata_payload_key: str,
    ) -> List[dict]:
        payloads = []
        for i, text in enumerate(texts):
            if text is None:
                raise ValueError(
                    "At least one of the texts is None. Please remove it before "
                    "calling .from_texts or .add_texts on Qdrant instance."
                )
            metadata = metadatas[i] if metadatas is not None else None
            payloads.append(
                {
                    content_payload_key: text,
                    metadata_payload_key: metadata,
                }
            )

        return payloads

    @classmethod
    def _document_from_scored_point(
        cls,
        scored_point: Any,
        content_payload_key: str,
        metadata_payload_key: str,
    ) -> Document:
        return Document(
            page_content=scored_point.payload.get(content_payload_key),
            metadata=scored_point.payload.get(metadata_payload_key) or {},
        )

    def _build_condition(self, key: str, value: Any) -> List[rest.FieldCondition]:
        from qdrant_client.http import models as rest

        out = []

        if isinstance(value, dict):
            for _key, value in value.items():
                out.extend(self._build_condition(f"{key}.{_key}", value))
        elif isinstance(value, list):
            for _value in value:
                if isinstance(_value, dict):
                    out.extend(self._build_condition(f"{key}[]", _value))
                else:
                    out.extend(self._build_condition(f"{key}", _value))
        else:
            out.append(
                rest.FieldCondition(
                    key=f"{self.metadata_payload_key}.{key}",
                    match=rest.MatchValue(value=value),
                )
            )

        return out

    def _qdrant_filter_from_dict(
        self, filter: Optional[DictFilter]
    ) -> Optional[rest.Filter]:
        from qdrant_client.http import models as rest

        if not filter:
            return None

        return rest.Filter(
            must=[
                condition
                for key, value in filter.items()
                for condition in self._build_condition(key, value)
            ]
        )
