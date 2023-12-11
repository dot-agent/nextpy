"""A flexbox container."""

from nextpy.frontend.components.libs.chakra import ChakraComponent
from nextpy.backend.vars import Var


class Container(ChakraComponent):
    """A flexbox container that centers its children and sets a max width."""

    tag = "Container"

    # If true, container will center its children regardless of their width.
    center_content: Var[bool]
