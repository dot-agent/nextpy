# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Declarative layout and common spacing props."""
from __future__ import annotations

from typing import Literal

from nextpy import el
from nextpy.backend.vars import Var

from .base import LayoutComponent

LiteralSectionSize = Literal["1", "2", "3"]


class Section(el.Section, LayoutComponent):
    """Denotes a section of page content."""

    tag = "Section"

    # The size of the section: "1" - "3" (default "3")
    size: Var[LiteralSectionSize]
