"""A flexbox container."""

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra import ChakraComponent


class Container(ChakraComponent):
    """A flexbox container that centers its children and sets a max width."""

    tag = "Container"

    # If true, container will center its children regardless of their width.
    center_content: Var[bool]
