"""Declarative layout and common spacing props."""
from __future__ import annotations

from nextpy.frontend import dom

from .base import LayoutComponent


class Box(dom.Div, LayoutComponent):
    """A fundamental layout building block, based on <div>."""

    tag = "Box"
