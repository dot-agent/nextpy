from __future__ import annotations
from typing import TYPE_CHECKING
from os import environ

# Conditional import for type checking
if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase

# Setting environment variable to control transformers verbosity
environ["TRANSFORMERS_VERBOSITY"] = "error"

from attr import define, field, Factory
from nextpy.ai.tokenizers import BaseTokenizer


@define(frozen=True)
class HuggingFaceTokenizer(BaseTokenizer):
    """
    Tokenizer class that wraps around a Hugging Face PreTrainedTokenizerBase
    to conform to the BaseTokenizer interface.
    """

    tokenizer: PreTrainedTokenizerBase = field(kw_only=True)
    max_tokens: int = field(
        default=Factory(lambda self: self.tokenizer.model_max_length, takes_self=True),
        kw_only=True,
    )

    def count_tokens(self, text: str) -> int:
        """
        Counts the number of tokens in the given text using the Hugging Face tokenizer.

        Args:
            text (str): The input text to tokenize.

        Returns:
            int: The number of tokens in the input text.
        """
        try:
            return len(self.tokenizer.encode(text))
        except Exception as e:
            # Log the exception or handle it as per your requirement
            raise RuntimeError(f"Error during tokenization: {e}")
