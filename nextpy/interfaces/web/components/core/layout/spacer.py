# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""A spacer component."""
from __future__ import annotations

from nextpy.interfaces.web.components.component import Component
from nextpy.interfaces.web.components.el.elements.typography import Div


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
