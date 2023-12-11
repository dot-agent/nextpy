from typing import Dict, Optional, Any
import json

from nextpy.ai.models.embedding.chroma import Chroma
from nextpy.ai.models.embedding.base import Embeddings

from . import BaseCache

class ChromaSemanticCache(BaseCache):
    """ChromaSemanticCache is a semantic cache that uses Chroma for caching."""

    def __init__(
        self,
        collection_name: str = "cache_collection",
        threshold: float = 0.2,
        embedding_function: Optional[Embeddings] = None
    ):
        self._cache_collection = Chroma(
            collection_name=collection_name, embedding_function=embedding_function
        )
        self._threshold = threshold

    def __getitem__(self, key: str) -> Any:
        """Get an item from the cache or throw key error."""
        response = self._cache_collection.similarity_search(query=key, top_k=1)
        if response and response[0][1] < self._threshold:
            # Deserialize JSON string to Python object
            return json.loads(response[0][0].metadata)
        else:
            raise KeyError(f"No data found for key: {key}")

    def __setitem__(self, key: str, value: Any) -> None:
        """Set an item in the cache."""
        # Serialize Python object to JSON string
        metadata = json.dumps({"prompt": key, "answer": value})
        self._cache_collection.add_texts(texts=[key], metadatas=[metadata])

    def __contains__(self, key: str) -> bool:
        """Check if a key is in the cache."""
        response = self._cache_collection.similarity_search(query=key, top_k=1)
        return response and response[0][1] < self._threshold

    def create_key(self, llm: str, **kwargs: Dict[str, Any]) -> str:
        """Create a lookup key for a call to the given llm with the given kwargs."""
        if "cache_key" in kwargs:
            return str(kwargs["cache_key"])
        elif "prompt" in kwargs:
            return str(kwargs["prompt"])
        else:
            raise ValueError("Expected 'cache_key' or 'prompt' in kwargs")

    def clear(self) -> None:
        """Clear the cache."""
        self._cache_collection.delete_collection()
