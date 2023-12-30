# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Tag to conditionally match cases."""

from typing import Any, List

from nextpy.backend.vars import Var
from nextpy.frontend.components.tags.tag import Tag


class MatchTag(Tag):
    """A match tag."""

    # The condition to determine which case to match.
    cond: Var[Any]

    # The list of match cases to be matched.
    match_cases: List[Any]

    # The catchall case to match.
    default: Any
