# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Container to stack elements with spacing."""

from typing import List, Union

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra import ChakraComponent, LiteralStackDirection


class Stack(ChakraComponent):
    """Container to stack elements with spacing."""

    tag = "Stack"

    # Shorthand for alignItems style prop
    align_items: Var[str]

    # The direction to stack the items.
    direction: Var[Union[LiteralStackDirection, List[str]]]

    # If true the items will be stacked horizontally.
    is_inline: Var[bool]

    # Shorthand for justifyContent style prop
    justify_content: Var[str]

    # If true, the children will be wrapped in a Box, and the Box will take the spacing props
    should_wrap_children: Var[bool]

    # The space between each stack item
    spacing: Var[str]

    # Shorthand for flexWrap style prop
    wrap: Var[str]

    # Alignment of contents.
    justify: Var[str]


class Hstack(Stack):
    """Stack items horizontally."""

    tag = "HStack"


class Vstack(Stack):
    """Stack items vertically."""

    tag = "VStack"
