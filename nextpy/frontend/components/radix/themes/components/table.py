"""Interactive components provided by @radix-ui/themes."""
from typing import Literal, Union

from nextpy.frontend import dom
from nextpy.backend.vars import Var

from ..base import (
    CommonMarginProps,
    RadixThemesComponent,
)


class TableRoot(dom.Table, CommonMarginProps, RadixThemesComponent):
    """Trigger an action or event, such as submitting a form or displaying a dialog."""

    tag = "Table.Root"

    # The size of the table: "1" | "2" | "3"
    size: Var[Literal[1, 2, 3]]

    # The variant of the table
    variant: Var[Literal["surface", "ghost"]]


class TableHeader(dom.Thead, CommonMarginProps, RadixThemesComponent):
    """Trigger an action or event, such as submitting a form or displaying a dialog."""

    tag = "Table.Header"


class TableRow(dom.Tr, CommonMarginProps, RadixThemesComponent):
    """Trigger an action or event, such as submitting a form or displaying a dialog."""

    tag = "Table.Row"

    # The alignment of the row
    align: Var[Literal["start", "center", "end", "baseline"]]


class TableColumnHeaderCell(dom.Th, CommonMarginProps, RadixThemesComponent):
    """Trigger an action or event, such as submitting a form or displaying a dialog."""

    tag = "Table.ColumnHeaderCell"

    # The justification of the column
    justify: Var[Literal["start", "center", "end"]]

    # width of the column
    width: Var[Union[str, int]]


class TableBody(dom.Tbody, CommonMarginProps, RadixThemesComponent):
    """Trigger an action or event, such as submitting a form or displaying a dialog."""

    tag = "Table.Body"


class TableCell(dom.Td, CommonMarginProps, RadixThemesComponent):
    """Trigger an action or event, such as submitting a form or displaying a dialog."""

    tag = "Table.Cell"

    # The justification of the column
    justify: Var[Literal["start", "center", "end"]]

    # width of the column
    width: Var[Union[str, int]]


class TableRowHeaderCell(dom.Th, CommonMarginProps, RadixThemesComponent):
    """Trigger an action or event, such as submitting a form or displaying a dialog."""

    tag = "Table.RowHeaderCell"

    # The justification of the column
    justify: Var[Literal["start", "center", "end"]]

    # width of the column
    width: Var[Union[str, int]]
