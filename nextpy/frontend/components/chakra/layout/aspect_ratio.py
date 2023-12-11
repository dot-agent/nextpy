"""A AspectRatio component."""

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra import ChakraComponent


class AspectRatio(ChakraComponent):
    """AspectRatio component is used to embed responsive videos and maps, etc."""

    tag = "AspectRatio"

    # The aspect ratio of the Box
    ratio: Var[float]
