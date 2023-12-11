"""A nextpyive container component."""

from typing import List, Union

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra import ChakraComponent


class Flex(ChakraComponent):
    """A nextpyive container component."""

    tag = "Flex"

    # How to align items in the flex.
    align: Var[str]

    # Shorthand for flexBasis style prop
    basis: Var[str]

    # Shorthand for flexDirection style prop
    direction: Var[Union[str, List[str]]]

    # Shorthand for flexGrow style prop
    grow: Var[str]

    # The way to justify the items.
    justify: Var[str]

    # Shorthand for flexWrap style prop
    wrap: Var[Union[str, List[str]]]

    # Shorthand for flexShrink style prop
    shrink: Var[str]
