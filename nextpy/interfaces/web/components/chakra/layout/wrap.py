# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Container to stack elements with spacing."""

from nextpy.backend.vars import Var
from nextpy.interfaces.web.components.chakra import ChakraComponent
from nextpy.interfaces.web.components.component import Component


class Wrap(ChakraComponent):
    """Layout component used to add space between elements and wrap automatically if there isn't enough space."""

    tag = "Wrap"

    # How to align the items.
    align: Var[str]

    # The flex direction of the wrap.
    direction: Var[str]

    # How to justify the items.
    justify: Var[str]

    # Whether to wrap children in `xt.wrap_item`.
    should_wrap_children: Var[bool]

    # The spacing between the items.
    spacing: Var[str]

    # The horizontal spacing between the items.
    spacing_x: Var[str]

    # The vertical spacing between the items.
    spacing_y: Var[str]

    @classmethod
    def create(cls, *children, items=None, **props) -> Component:
        """Return a wrap component.

        Args:
            *children: The children of the component.
            items (list): The items of the wrap component.
            **props: The properties of the component.

        Returns:
            The wrap component.
        """
        if len(children) == 0:
            children = []
            for item in items or []:
                children.append(WrapItem.create(*item))

        return super().create(*children, **props)


class WrapItem(ChakraComponent):
    """Item of the Wrap component."""

    tag = "WrapItem"
