"""A spacer component."""
from __future__ import annotations

from nextpy.frontend.components.component import Component
from nextpy.frontend.components.el.elements.typography import Div


class Spacer(Div):
    """A spacer component."""

    def _apply_theme(self, theme: Component | None):
        self.style.update(
            {
                "flex": 1,
                "justify_self": "stretch",
                "align_self": "stretch",
            }
        )


spacer = Spacer.create
