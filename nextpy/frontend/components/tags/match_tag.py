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
