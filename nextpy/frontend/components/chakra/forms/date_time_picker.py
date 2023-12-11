"""A datetime-local input component."""

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra.forms.input import Input


class DateTimePicker(Input):
    """A datetime-local input component."""

    # The type of input.
    type_: Var[str] = "datetime-local"  # type: ignore
