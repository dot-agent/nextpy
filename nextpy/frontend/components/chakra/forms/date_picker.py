"""A date input component."""

from nextpy.backend.vars import Var
from nextpy.frontend.components.chakra.forms.input import Input


class DatePicker(Input):
    """A date input component."""

    # The type of input.
    type_: Var[str] = "date"  # type: ignore
