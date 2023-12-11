from __future__ import annotations
from attr import define, field, Factory
from abc import ABC, abstractmethod


@define(frozen=True)
class BaseTokenizer(ABC):
    """Abstract base class for a tokenizer."""

    # Define RESPONSE_STOP_SEQUENCE as a class attribute
    RESPONSE_STOP_SEQUENCE = "<|Response|>"

    stop_sequences: list[str] = field(
        default=Factory(lambda: [BaseTokenizer.RESPONSE_STOP_SEQUENCE]), kw_only=True
    )

    @property
    @abstractmethod
    def max_tokens(self) -> int:
        """Abstract property to get the maximum number of tokens."""
        pass

    def count_tokens_left(self, text: str | list[str]) -> int:
        """Calculate the number of tokens left within the max_tokens limit."""
        remaining = self.max_tokens - self.count_tokens(text)
        return max(0, remaining)

    @abstractmethod
    def count_tokens(self, text: str | list[str]) -> int:
        """Abstract method to count the number of tokens in the given text."""
        pass
