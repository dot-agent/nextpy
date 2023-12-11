"""An email input component."""

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra.forms.input import Input


class Email(Input):
    """An email input component."""

    # The type of input.
    type_: Var[str] = "email"  # type: ignore
