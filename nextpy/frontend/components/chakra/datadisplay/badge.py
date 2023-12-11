"""Badge component."""

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra import ChakraComponent, LiteralVariant


class Badge(ChakraComponent):
    """A badge component."""

    tag = "Badge"

    # Variant of the badge ("solid" | "subtle" | "outline")
    variant: Var[LiteralVariant]

    # The color of the badge
    color_scheme: Var[str]
