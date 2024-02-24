# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""A line to divide parts of the layout."""
from typing import Literal

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra import ChakraComponent, LiteralDividerVariant

LiteralLayout = Literal["horizontal", "vertical"]


class Divider(ChakraComponent):
    """Dividers are used to visually separate content in a list or group."""

    tag = "Divider"

    # Pass the orientation prop and set it to either horizontal or vertical. If the vertical orientation is used, make sure that the parent element is assigned a height.
    orientation: Var[LiteralLayout]

    # Variant of the divider ("solid" | "dashed")
    variant: Var[LiteralDividerVariant]
