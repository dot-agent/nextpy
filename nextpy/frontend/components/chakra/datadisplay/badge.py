# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

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
