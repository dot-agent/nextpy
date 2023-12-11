"""A datetime-local input component."""

from nextpy.frontend.components.forms.input import Input
from nextpy.backend.vars import Var


class DateTimePicker(Input):
    """A datetime-local input component."""

    # The type of input.
    type_: Var[str] = "datetime-local"  # type: ignore
