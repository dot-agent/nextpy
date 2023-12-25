"""A password input component."""

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra.forms.input import Input


class Password(Input):
    """A password input component."""

    # The type of input.
    type_: Var[str] = "password"  # type: ignore
