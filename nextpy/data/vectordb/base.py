from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional, Tuple

from nextpy.ai.models.embedding.base import Embeddings
from nextpy.ai.schema import Document


class VectorDB(ABC):
    """Interface for vector stores."""

    @abstractmethod
    def add_texts(
        self,
        texts: Iterable[str],
        metadatas: Optional[list[dict]] = None,
        **kwargs: Any,
    ) -> list[str]:
        """Run more texts through the Embedding and add to the vectordb.

        Args:
            texts: Iterable of strings to add to the vectordb.
            metadatas: Optional list of metadatas associated with the texts.
            kwargs: vectordb specific parameters.

        Returns:
            List of ids from adding the texts into the vectordb.
        """
        pass

    def add_documents(self, documents: list[Document], **kwargs: Any) -> list[str]:
        """Run more documents through the Embedding and add to the vectordb.

        Args:
            documents: Documents to add to the vectordb.

        Returns:
            List of IDs of the added texts.
        """
        # TODO: Handle the case where the user doesn't provide ids on the Collection
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        return self.add_texts(texts, metadatas, **kwargs)

    @abstractmethod
    def similarity_search(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> list[Document]:
        """Return documents most similar to query."""
        pass

    def get_matching_text_with_score(
        self, query: str, k: int = 4, **kwargs: Any
    ) -> list[Tuple[Document, float]]:
        """Return documents and relevance scores in the range [0, 1].
        0 is dissimilar, 1 is most similar.

        Args:
            query: Input text.
            k: Number of Documents to return. Defaults to 4.
             **kwargs: kwargs to be passed to similarity search, may include core_threshold: Optional, a floating point value between 0 to 1 to
                    filter the resulting set of retrieved docs

        Returns:
            List of Tuples of (doc, similarity_score).
        """
        docs_and_similarities = self._similarity_search_with_relevance_scores(
            query, k=k, **kwargs
        )
        if any(
            similarity < 0.0 or similarity > 1.0
            for _, similarity in docs_and_similarities
        ):
            warnings.warn(
                "Relevance scores must be between"
                f" 0 and 1, got {docs_and_similarities}"
            )

        score_threshold = kwargs.get("score_threshold")
        if score_threshold is not None:
            docs_and_similarities = [
                (doc, similarity)
                for doc, similarity in docs_and_similarities
                if similarity >= score_threshold
            ]
            if len(docs_and_similarities) == 0:
                warnings.warn(
                    f"No relevant docs were retrieved using the relevance score\
                          threshold {score_threshold}"
                )
        return docs_and_similarities

    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        embedding: Embeddings,
        **kwargs: Any,
    ):
        """Return VectorDB initialized from documents and Embedding."""
        texts = [d.page_content for d in documents]
        metadatas = [d.metadata for d in documents]
        return cls.from_texts(texts, embedding, metadatas=metadatas, **kwargs)

    @classmethod
    @abstractmethod
    def from_texts(
        cls,
        texts: list[str],
        embedding: Embeddings,
        metadatas: Optional[list[dict]] = None,
        **kwargs: Any,
    ):
        """Return VectorDB initialized from texts and Embedding."""
        pass
