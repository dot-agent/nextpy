from typing import List, Optional, Union

import reacton.ipyvuetify as v

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.util import _combine_classes


@widget.component
def success(
    label: Optional[str] = None,
    icon: Union[bool, str, None] = True,
    dense=False,
    outlined=True,
    text=True,
    children=[],
    classes: List[str] = [],
    **kwargs,
):
    """Display a success message (green color).

    ## Arguments

     * `label`: the message to display
     * `icon`: if True, display a check icon, if False, don't display an icon, if a string,
               display the icon with that name ([Overview of available icons](https://pictogrammers.github.io/@mdi/font/4.9.95/)).
     * `dense`: if True, display the message in a dense format, using less vertical height.
     * `outlined`: if True (default), display the message in an outlined border, instead of a filled box.
     * `text`: if True (default), display the message in a text format, which applies a semi-transparent background.
     * `classes`: additional CSS classes to apply.
    """
    # vuetify doesn't accept True, but is ok with None for a default icon
    if icon is True:
        icon = None
    return v.Alert(
        type="success",
        text=text,
        outlined=outlined,
        dense=dense,
        icon=icon,
        children=[*([label] if label is not None else []), *children],
        class_=_combine_classes(classes),
        **kwargs,
    )


@widget.component
def info(
    label: Optional[str] = None,
    icon: Union[bool, str, None] = True,
    dense=False,
    outlined=True,
    text=True,
    children=[],
    classes: List[str] = [],
    **kwargs,
):
    """Display a info message (blue color).

    ## Arguments

     * `label`: the message to display
     * `icon`: if True, display a info icon, if False, don't display an icon, if a string,
               display the icon with that name ([Overview of available icons](https://pictogrammers.github.io/@mdi/font/4.9.95/)).
     * `dense`: if True, display the message in a dense format, using less vertical height.
     * `outlined`: if True (default), display the message in an outlined border, instead of a filled box.
     * `text`: if True (default), display the message in a text format, which applies a semi-transparent background.
     * `classes`: additional CSS classes to apply.
    """
    if icon is True:
        icon = None
    return v.Alert(
        type="info",
        text=text,
        outlined=outlined,
        dense=dense,
        icon=icon,
        children=[*([label] if label is not None else []), *children],
        class_=_combine_classes(classes),
        **kwargs,
    )


@widget.component
def warning(
    label: Optional[str] = None,
    icon: Union[bool, str, None] = True,
    dense=False,
    outlined=True,
    text=True,
    children=[],
    classes: List[str] = [],
    **kwargs,
):
    """Display a warning message (orange color).

    ## Arguments

     * `label`: the message to display
     * `icon`: if True, display a exclamation icon, if False, don't display an icon, if a string,
               display the icon with that name ([Overview of available icons](https://pictogrammers.github.io/@mdi/font/4.9.95/)).
     * `dense`: if True, display the message in a dense format, using less vertical height.
     * `outlined`: if True (default), display the message in an outlined border, instead of a filled box.
     * `text`: if True (default), display the message in a text format, which applies a semi-transparent background.
     * `classes`: additional CSS classes to apply.
    """
    if icon is True:
        icon = None
    return v.Alert(
        type="warning",
        text=text,
        outlined=outlined,
        dense=dense,
        icon=icon,
        children=[*([label] if label is not None else []), *children],
        class_=_combine_classes(classes),
        **kwargs,
    )


@widget.component
def error(
    label: Optional[str] = None,
    icon: Union[bool, str, None] = True,
    dense=False,
    outlined=True,
    text=True,
    children=[],
    classes: List[str] = [],
    **kwargs,
):
    """Display an error message (red color).

    ## Arguments

     * `label`: the message to display
     * `icon`: if True, display a exclamation in a red triangle icon, if False, don't display an icon, if a string,
               display the icon with that name ([Overview of available icons](https://pictogrammers.github.io/@mdi/font/4.9.95/)).
     * `dense`: if True, display the message in a dense format, using less vertical height.
     * `outlined`: if True (default), display the message in an outlined border, instead of a filled box.
     * `text`: if True (default), display the message in a text format, which applies a semi-transparent background.
     * `classes`: additional CSS classes to apply.
    """
    if icon is True:
        icon = None
    return v.Alert(
        type="error",
        text=text,
        outlined=outlined,
        dense=dense,
        icon=icon,
        children=[*([label] if label is not None else []), *children],
        class_=_combine_classes(classes),
        **kwargs,
    )
