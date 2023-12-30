# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Link overlay components."""

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra import ChakraComponent


class LinkOverlay(ChakraComponent):
    """Wraps child component in a link."""

    tag = "LinkOverlay"

    # If true, the link will open in new tab
    is_external: Var[bool]

    # Href of the link overlay.
    href: Var[str]


class LinkBox(ChakraComponent):
    """The LinkBox lifts any nested links to the top using z-index to ensure proper keyboard navigation between links."""

    tag = "LinkBox"
