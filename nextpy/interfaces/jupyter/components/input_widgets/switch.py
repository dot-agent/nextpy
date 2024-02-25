from typing import Callable, Dict, List, Optional, Union

import reacton.ipyvuetify as v

import nextpy.interfaces.jupyter as widget


@widget.value_component(bool)
def switch(
    *,
    label: str = None,
    value: Union[bool, widget.Reactive[bool]] = True,
    on_value: Callable[[bool], None] = None,
    disabled: bool = False,
    children: list = [],
    classes: List[str] = [],
    style: Optional[Union[str, Dict[str, str]]] = None,
):
    """A switch component provides users the ability to choose between two distinct values. But aesthetically different from a checkbox.

    Basic examples

    ```widget
    import nextpy.interfaces.jupyter

    show_message = widget.reactive(True)
    disable = widget.reactive(False)


    @widget.component
    def Page():
        with widget.column():
            with widget.row():
                widget.switch(label="Hide Message", value=show_message, disabled=disable.value)
                widget.switch(label="Disable Message switch", value=disable)

            if show_message.value:
                widget.Markdown("## Use switch to show/hide message")

    ```


    ## Arguments

     * `label`: The label to display next to the switch.
     * `value`: The current value of the switch (True or False).
     * `on_value`: A callback that is called when the switch is toggled.
     * `disabled`: If True, the switch is disabled and cannot be used.
     * `children`: A list of child elements to display on the switch.
     * `classes`: Additional CSS classes to apply.
     * `style`: CSS style to apply.

    """
    reactive_value = widget.use_reactive(value, on_value)
    del value, on_value

    if label:
        children = [label] + children

    return v.Switch(
        label=label,
        v_model=reactive_value.value,
        on_v_model=reactive_value.set,
        disabled=disabled,
        class_=widget.util._combine_classes(classes),
        style_=widget.util._flatten_style(style),
        children=children,
    )
