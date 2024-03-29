# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Typography components."""

from nextpy.interfaces.web.components.component import Component
from .header import Header 
from .heading import Heading
from .highlight import Highlight
from .span import Span
from .subheader import SubHeader
from .text import Text
from .title import Title 

__all__ = [f for f in dir() if f[0].isupper() or f in ("span",)]  # type: ignore
