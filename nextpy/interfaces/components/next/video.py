# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Wrapping of the next-video component."""

from typing import Optional

from nextpy.backend.vars import Var
from nextpy.frontend.components.component import Component

from .base import NextComponent


class Video(NextComponent):
    """A video component from NextJS."""

    tag = "Video"
    library = "next-video"
    is_default = True
    # the URL
    src: Var[str]

    as_: Optional[Component]

    @classmethod
    def create(cls, *children, **props) -> NextComponent:
        """Create a Video component.

        Args:
            *children: The children of the component.
            **props: The props of the component.

        Returns:
            The Video component.
        """
        return super().create(*children, **props)
