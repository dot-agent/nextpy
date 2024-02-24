# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""A component to display visually hidden text."""

from nextpy.frontend.components.chakra import ChakraComponent


class VisuallyHidden(ChakraComponent):
    """A component that visually hides content while still allowing it to be read by screen readers."""

    tag = "VisuallyHidden"
