"""Components for rendering heading.

https://www.radix-ui.com/themes/docs/theme/typography
"""
from __future__ import annotations

from nextpy.frontend import dom
from nextpy.backend.vars import Var

from ..base import (
    CommonMarginProps,
    RadixThemesComponent,
)
from .base import (
    LiteralTextSize,
)


class Kbd(dom.Kbd, CommonMarginProps, RadixThemesComponent):
    """Represents keyboard input or a hotkey."""

    tag = "Kbd"

    # Text size: "1" - "9"
    size: Var[LiteralTextSize]
