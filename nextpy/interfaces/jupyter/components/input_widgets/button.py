from typing import Callable, Dict, List, Optional, Union

from reacton import ipyvue
from reacton import ipyvuetify as v

import nextpy.interfaces.jupyter as widget

"""A button that can be clicked to trigger an event.

    ## Example

    ```widget
    import nextpy.interfaces.jupyter as widget

    @widget.component
    def Page():
        with widget.row():
            widget.button(label="Default")
            widget.button(label="Default+color", color="primary")
            widget.button(label="text", text=True)
            widget.button(label="Outlined", outlined=True)
            widget.button(label="Outlined+color", outlined=True, color="primary")
    ```
    ## Arguments

    - `label`: The text to display on the button.
    - `on_click`: A callback function that is called when the button is clicked.
    - `icon_name`: The name of the icon to display on the button ([Overview of available icons](https://pictogrammers.github.io/@mdi/font/4.9.95/)).
    - `children`: A list of child elements to display on the button.
    - `disabled`: Whether the button is disabled.
    - `text`: Whether the button should be displayed as text, it has no shadow and no background.
    - `outlined`: Whether the button should be displayed as outlined, it has no background.
    - `value`: (Optional) When used as a child of a ToggleButtons component, the value of the selected button, see [ToggleButtons](/api/togglebuttons).
    - `classes`: Additional CSS classes to apply.
    - `style`: CSS style to apply.
    
    """

@widget.component
def button(
    label: str = None,
    on_click: Callable[[], None] = None,
    icon_name: str = None,
    children: list = [],
    disabled: bool = False,
    text: bool = False,
    outlined: bool = False,
    color: Optional[str] = None,
    click_event: str = "click",
    class_name: str = '',
    style: str = '',
    value=None,
    **kwargs,
):
    if label:
        children = [label] + children
    if icon_name:
        children = [v.Icon(left=bool(label), children=[icon_name])] + children
    kwargs = kwargs.copy()
    if widget.util.ipyvuetify_major_version == 3:
        variant = "elevated"
        if text:
            variant = "text"
        elif outlined:
            variant = "outlined"
        btn = widget.v.Btn(children=children, **kwargs, disabled=disabled, class_=class_name, style_=style, color=color, variant=variant)
    else:
        btn = widget.v.Btn(children=children, **kwargs, disabled=disabled, text=text, class_=class_name, style_=style, outlined=outlined, color=color)
    ipyvue.use_event(btn, click_event, lambda *_ignore: on_click and on_click())
    return btn
