from typing import Callable, Dict, List, Optional, TypeVar, Union, cast, overload

import ipyvuetify as v
import reacton.core

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.alias import rv
from nextpy.interfaces.jupyter.util import _combine_classes

T = TypeVar("T")


@widget.value_component(None)
def select_box(
    label: str,
    values: List[T],
    value: Union[None, T, widget.Reactive[T], widget.Reactive[Optional[T]]] = None,
    on_value: Union[None, Callable[[T], None], Callable[[Optional[T]], None]] = None,
    dense: bool = False,
    disabled: bool = False,
    class_name : str = '',
    style: str = ''
) -> reacton.core.ValueElement[v.Select, T]:
    """Select a single value from a list of values.

    ### Basic example:

    ```widget
    import nextpy.interfaces.jupyter

    foods = ["Kiwi", "Banana", "Apple"]
    food = widget.reactive("Banana")


    @widget.component
    def Page():
        widget.Select(label="Food", value=food, values=foods)
        widget.Markdown(f"**Selected**: {food.value}")
    ```

    ## Arguments

     * `label`: Label to display next to the select.
     * `value`: The currently selected value.
     * `values`: List of values to select from.
     * `on_value`: Callback to call when the value changes.
     * `dense`: Whether to use a denser style.
     * `disabled`: Whether the select widget allow user interaction
     * `classes`: List of CSS classes to apply to the select.
     * `style`: CSS style to apply to the select.

    """
    # next line is very hard to get right with typing
    # might need an overload on use_reactive, when value is None
    reactive_value = widget.use_reactive(value, on_value)  # type: ignore
    del value, on_value
    return cast(
        reacton.core.ValueElement[v.Select, T],
        rv.Select(
            v_model=reactive_value.value,
            on_v_model=reactive_value.set,
            items=values,
            label=label,
            dense=dense,
            disabled=disabled,
            class_=class_name,
            style_=style,
        ),
    )