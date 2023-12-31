# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import json
import hashlib
from typing import Any, Dict
from abc import ABC, abstractmethod

class BaseCache(ABC):
    @abstractmethod
    def __getitem__(self, key: str) -> Any:
        """get an item from the cache or throw key error"""
        pass

    @abstractmethod
    def __setitem__(self, key: str, value: Any) -> None:
        """set an item in the cache"""
        pass

    @abstractmethod
    def __contains__(self, key: str) -> bool:
        """see if we can return a cached value for the passed key"""
        pass

    def create_key(self, llm: str, **kwargs: Dict[str, Any]) -> str:
        """Define a lookup key for a call to the given llm with the given kwargs.
        One of the keyword args could be `cache_key` in which case this function should respect that
        and use it.
        """
        if "cache_key" in kwargs:
            return str(kwargs["cache_key"])

        hasher = hashlib.md5()
        options_str = json.dumps(kwargs, sort_keys=True)

        combined = "{}{}".format(llm, options_str).encode()

        hasher.update(combined)
        return hasher.hexdigest()

    @abstractmethod
    def clear(self):
        """Clear cache"""
        pass
