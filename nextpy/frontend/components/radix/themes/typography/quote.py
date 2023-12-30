# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Components for rendering heading.

https://www.radix-ui.com/themes/docs/theme/typography
"""
from __future__ import annotations

from nextpy import el

from ..base import (
    CommonMarginProps,
    RadixThemesComponent,
)


class Quote(el.Q, CommonMarginProps, RadixThemesComponent):
    """A short inline quotation."""

    tag = "Quote"
