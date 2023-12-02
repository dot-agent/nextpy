from typing import Any

from . import BaseCache

class LocalMemoryCache(BaseCache):
    def __init__(self) -> None:
        """Initialize an empty memory cache."""
        self._memory_cache = {}

    def __getitem__(self, key: str) -> Any:
        """Get the value for a key. Raise KeyError if the key is not found."""
        try:
            return self._memory_cache[key]
        except KeyError:
            raise KeyError(f"Key {key} not found in cache.")

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a value for a key in the memory cache."""
        self._memory_cache[key] = value

    def __contains__(self, key: str) -> bool:
        """Check if a key is in the memory cache."""
        return key in self._memory_cache

    def clear(self) -> None:
        """Clear the memory cache."""
        self._memory_cache = {}
