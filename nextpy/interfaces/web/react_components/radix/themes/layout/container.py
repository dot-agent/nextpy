# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Declarative layout and common spacing props."""
from __future__ import annotations

from typing import Literal

from nextpy import el
from nextpy.backend.vars import Var

from .base import LayoutComponent

LiteralContainerSize = Literal["1", "2", "3", "4"]


class Container(el.Div, LayoutComponent):
    """Constrains the maximum width of page content.

    See https://www.radix-ui.com/themes/docs/components/container
    """

    tag = "Container"

    # The size of the container: "1" - "4" (default "4")
    size: Var[LiteralContainerSize]
