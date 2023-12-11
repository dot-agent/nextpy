"""Components for rendering heading.

https://www.radix-ui.com/themes/docs/theme/typography
"""
from __future__ import annotations

from nextpy.frontend import dom

from ..base import (
    CommonMarginProps,
    RadixThemesComponent,
)


class Strong(dom.Strong, CommonMarginProps, RadixThemesComponent):
    """Marks text to signify strong importance."""

    tag = "Strong"
