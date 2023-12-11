"""Components for rendering heading.

https://www.radix-ui.com/themes/docs/theme/typography
"""
from __future__ import annotations

from nextpy.frontend import dom

from ..base import (
    CommonMarginProps,
    RadixThemesComponent,
)


class Em(dom.Em, CommonMarginProps, RadixThemesComponent):
    """Marks text to stress emphasis."""

    tag = "Em"
