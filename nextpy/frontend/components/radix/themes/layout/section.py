"""Declarative layout and common spacing props."""
from __future__ import annotations

from typing import Literal

from nextpy.frontend import dom
from nextpy.backend.vars import Var

from .base import LayoutComponent

LiteralSectionSize = Literal["1", "2", "3"]


class Section(dom.Section, LayoutComponent):
    """Denotes a section of page content."""

    tag = "Section"

    # The size of the section: "1" - "3" (default "3")
    size: Var[LiteralSectionSize]
