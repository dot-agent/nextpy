# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Top-level component that wraps the entire app."""
from nextpy.backend.vars import Var
from nextpy.frontend.components.base.fragment import Fragment
from nextpy.frontend.components.component import Component


class AppWrap(Fragment):
    """Top-level component that wraps the entire app."""

    @classmethod
    def create(cls) -> Component:
        """Create a new AppWrap component.

        Returns:
            A new AppWrap component containing {children}.
        """
        return super().create(
            Var.create("{children}", _var_is_local=False, _var_is_string=False)
        )
