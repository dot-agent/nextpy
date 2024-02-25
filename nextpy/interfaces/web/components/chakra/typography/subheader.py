"""A subheader component."""

from nextpy.backend.vars import Var
from nextpy.interfaces.web.components.chakra import ChakraComponent, LiteralHeadingSize

class SubHeader(ChakraComponent):
    """A page heading."""

    tag = "Heading"

    # Override the tag. The default tag is `<h2>`.
    as_: Var[str]

    # "4xl" | "3xl" | "2xl" | "xl" | "lg" | "md" | "sm" | "xs"
    size: Var[LiteralHeadingSize] = "xl"

