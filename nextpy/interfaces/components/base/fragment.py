# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""React fragments to enable bare returns of component trees from functions."""
from nextpy.frontend.components.component import Component


class Fragment(Component):
    """A React fragment to return multiple components from a function without wrapping it in a container."""

    library = "react"
    tag = "Fragment"
