# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""A text component."""
from __future__ import annotations

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra import ChakraComponent


class Text(ChakraComponent):
    """Render a paragraph of text."""

    tag = "Text"

    # Override the tag. The default tag is `<p>`.
    as_: Var[str]

    # Truncate text after a specific number of lines. It will render an ellipsis when the text exceeds the width of the viewport or max_width prop.
    no_of_lines: Var[int]
