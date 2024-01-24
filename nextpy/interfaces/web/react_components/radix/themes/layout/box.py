# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Declarative layout and common spacing props."""
from __future__ import annotations

from nextpy import el

from .base import LayoutComponent


class Box(el.Div, LayoutComponent):
    """A fundamental layout building block, based on <div>."""

    tag = "Box"
