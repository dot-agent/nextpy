# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Base class definition for raw HTML elements."""


from nextpy.frontend.components.component import Component


class Element(Component):
    """The base class for all raw HTML elements."""

    def __eq__(self, other):
        """Two elements are equal if they have the same tag.

        Args:
            other: The other element.

        Returns:
            True if the elements have the same tag, False otherwise.
        """
        return isinstance(other, Element) and self.tag == other.tag
