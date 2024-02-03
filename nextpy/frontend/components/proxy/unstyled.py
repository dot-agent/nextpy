"""Unstyled Components Alias."""
# File: nextpy/frontend/components/proxy/unstyled.py

import sys
from nextpy.frontend.components.radix.themes import *
from nextpy.frontend.components.radix.themes.components import *
from nextpy.frontend.components.radix.themes.layout import *
from nextpy.frontend.components.radix.themes.typography import *
from nextpy.frontend.components.radix.primitives import *

class Unstyled:
    def __getattr__(self, item):
        # Check in each submodule for the component
        for module in [themes, components, layout, typography, primitives]:
            try:
                return getattr(module, item)
            except AttributeError:
                continue
        # If not found, raise an attribute error
        raise AttributeError(f"No component named '{item}' in unstyled module")

# Create an instance of the Unstyled class
unstyled = Unstyled()

# Optionally, you can define __all__ for explicit exports
__all__ = [name for name in dir() if not name.startswith("_") and name != 'Unstyled']
