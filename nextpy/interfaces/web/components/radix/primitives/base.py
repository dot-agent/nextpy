# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""The base component for Radix primitives."""
from typing import List

from nextpy.backend.vars import Var
from nextpy.interfaces.web.components.component import Component
from nextpy.interfaces.web.components.tags.tag import Tag
from nextpy.utils import format


class RadixPrimitiveComponent(Component):
    """Basic component for radix Primitives."""

    # Change the default rendered element for the one passed as a child.
    as_child: Var[bool]

    lib_dependencies: List[str] = ["@emotion/react@^11.11.1"]

    def _render(self) -> Tag:
        return (
            super()
            ._render()
            .add_props(
                **{
                    "class_name": format.to_title_case(self.tag or ""),
                }
            )
        )
