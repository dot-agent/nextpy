# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""A highlight component."""

from typing import Dict, List

from nextpy.backend.vars import Var
from nextpy.interfaces.web.components.chakra import ChakraComponent
from nextpy.interfaces.web.components.tags import Tag


class Highlight(ChakraComponent):
    """Highlights a specific part of a string."""

    tag = "Highlight"

    # A query for the text to highlight. Can be a string or a list of strings.
    query: Var[List[str]]

    # The style of the content.
    # Note: styles and style are different prop.
    styles: Var[Dict] = {"px": "2", "py": "1", "rounded": "full", "bg": "teal.100"}  # type: ignore

    def _render(self) -> Tag:
        return super()._render().add_props(styles=self.style)
