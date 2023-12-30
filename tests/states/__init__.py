# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Common xt.BaseState subclasses for use in tests."""
import nextpy as xt
from nextpy.backend.state import BaseState

from .mutation import DictMutationTestState, ListMutationTestState, MutableTestState
from .upload import (
    ChildFileUploadState,
    FileStateBase1,
    FileStateBase2,
    FileUploadState,
    GrandChildFileUploadState,
    SubUploadState,
    UploadState,
)


class GenState(BaseState):
    """A state with event handlers that generate multiple updates."""

    value: int

    def go(self, c: int):
        """Increment the value c times and update each time.

        Args:
            c: The number of times to increment.

        Yields:
            After each increment.
        """
        for _ in range(c):
            self.value += 1
            yield
