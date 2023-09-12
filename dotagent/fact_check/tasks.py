"""Definition of different types of tasks."""
from __future__ import annotations

from enum import Enum


class TaskType(str, Enum):
    """Task types available in this tool."""

    kbqa = "kbqa"
    math = "math"
    code = "code"
    sci = "sci"

    @staticmethod
    def list() -> list[str]:
        """Obtains string representations of all values.
        Returns:
            List of all values in str.
        """
        return list(map(lambda c: c.value, TaskType))