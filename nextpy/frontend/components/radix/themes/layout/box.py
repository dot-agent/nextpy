"""Declarative layout and common spacing props."""
from __future__ import annotations

from nextpy import el

from .base import LayoutComponent


class Box(el.Div, LayoutComponent):
    """A fundamental layout building block, based on <div>."""

    tag = "Box"
