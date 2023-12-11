"""A password input component."""

from nextpy.frontend.components.forms.input import Input
from nextpy.backend.vars import Var


class Password(Input):
    """A password input component."""

    # The type of input.
    type_: Var[str] = "password"  # type: ignore
