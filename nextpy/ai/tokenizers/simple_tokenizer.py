from attr import define, field
from nextpy.ai.tokenizers import BaseTokenizer


@define(frozen=True)
class SimpleTokenizer(BaseTokenizer):
    """
    A simple tokenizer that divides the input text into tokens based on the number of characters per token.
    """

    characters_per_token: int = field(kw_only=True)
    max_tokens: int = field(kw_only=True)

    def count_tokens(self, text: str) -> int:
        """
        Count the number of tokens in the given text based on the predefined number of characters per token.

        Args:
            text (str): The input text to be tokenized.

        Returns:
            int: The number of tokens in the input text.
        """
        if self.characters_per_token <= 0:
            raise ValueError("characters_per_token must be a positive integer")

        num_tokens = (
            len(text) + self.characters_per_token - 1
        ) // self.characters_per_token
        return num_tokens
