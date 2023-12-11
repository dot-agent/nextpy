"""A AspectRatio component."""

from nextpy.frontend.components.libs.chakra import ChakraComponent
from nextpy.backend.vars import Var


class AspectRatio(ChakraComponent):
    """AspectRatio component is used to embed responsive videos and maps, etc."""

    tag = "AspectRatio"

    # The aspect ratio of the Box
    ratio: Var[float]
