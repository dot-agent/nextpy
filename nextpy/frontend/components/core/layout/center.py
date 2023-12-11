"""A center component."""
from __future__ import annotations

from nextpy.frontend.components.component import Component
from nextpy.frontend.components.el.elements.typography import Div


class Center(Div):
    """A center component."""

    def _apply_theme(self, theme: Component | None):
        self.style.update(
            {
                "display": "flex",
                "align_items": "center",
                "justify_content": "center",
            }
        )


center = Center.create
