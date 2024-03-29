# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Declarative layout and common spacing props."""
from __future__ import annotations

from typing import Literal

from nextpy.interfaces.web.components import el
from nextpy.backend.vars import Var

from ..base import (
    LiteralAlign,
    LiteralJustify,
    LiteralSize,
)
from .base import LayoutComponent

LiteralFlexDirection = Literal["row", "column", "row-reverse", "column-reverse"]
LiteralFlexDisplay = Literal["none", "inline-flex", "flex"]
LiteralFlexWrap = Literal["nowrap", "wrap", "wrap-reverse"]


class Flex(el.Div, LayoutComponent):
    """Component for creating flex layouts."""

    tag = "Flex"

    # Change the default rendered element for the one passed as a child, merging their props and behavior.
    as_child: Var[bool]

    # How to display the element: "none" | "inline-flex" | "flex"
    display: Var[LiteralFlexDisplay]

    # How child items are layed out: "row" | "column" | "row-reverse" | "column-reverse"
    direction: Var[LiteralFlexDirection]

    # Alignment of children along the main axis: "start" | "center" | "end" | "baseline" | "stretch"
    align: Var[LiteralAlign]

    # Alignment of children along the cross axis: "start" | "center" | "end" | "between"
    justify: Var[LiteralJustify]

    # Whether children should wrap when they reach the end of their container: "nowrap" | "wrap" | "wrap-reverse"
    wrap: Var[LiteralFlexWrap]

    # Gap between children: "0" - "9"
    gap: Var[LiteralSize]
