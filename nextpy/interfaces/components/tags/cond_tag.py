# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Tag to conditionally render components."""

from typing import Any, Dict, Optional

from nextpy.backend.vars import Var
from nextpy.frontend.components.tags.tag import Tag


class CondTag(Tag):
    """A conditional tag."""

    # The condition to determine which component to render.
    cond: Var[Any]

    # The code to render if the condition is true.
    true_value: Dict

    # The code to render if the condition is false.
    false_value: Optional[Dict]
