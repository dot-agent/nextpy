"""A span component."""
from __future__ import annotations

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra import ChakraComponent


class Span(ChakraComponent):
    """Render an inline span of text."""

    tag = "Text"

    # Override the tag. The default tag is `<span>`.
    as_: Var[str] = "span"  # type: ignore
