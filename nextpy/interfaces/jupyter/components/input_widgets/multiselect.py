from typing import Callable, Dict, List, Optional, TypeVar, Union, cast, overload

import ipyvuetify as v
import reacton.core

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.alias import rv
from nextpy.interfaces.jupyter.util import _combine_classes

T = TypeVar("T")

@widget.value_component(None)
def multiselect(
    label: str,
    values: List[T],
    all_values: List[T],
    on_value: Callable[[List[T]], None] = None,
    dense: bool = False,
    disabled: bool = False,
    class_name: str = '',
    style: str = '',
) -> reacton.core.ValueElement[v.Select, List[T]]:
    """Select multiple values from a list of values.

    ### Basic example:

    ```widget
    import nextpy.interfaces.jupyter

    all_languages = "Python C++ Java JavaScript TypeScript BASIC".split()
    languages = widget.reactive([all_languages[0]])


    @widget.component
    def Page():
        widget.SelectMultiple("Languages", languages, all_languages)
        widget.Markdown(f"**Selected**: {languages.value}")
    ```

    ## Arguments

     * `label`: Label to display next to the select.
     * `values`: List of currently selected values.
     * `all_values`: List of all values to select from.
     * `on_value`: Callback to call when the value changes.
     * `dense`: Whether to use a denser style.
     * `disabled`: Whether the select widget allow user interaction
     * `classes`: List of CSS classes to apply to the select.
     * `style`: CSS style to apply to the select.
    """
    reactive_values = widget.use_reactive(values, on_value)
    del values, on_value

    return cast(
        reacton.core.ValueElement[v.Select, List[T]],
        rv.Select(
            v_model=reactive_values.value,
            on_v_model=reactive_values.set,
            items=all_values,
            label=label,
            multiple=True,
            dense=False,
            disabled=disabled,
            class_=class_name,
            style_=style,
        ),
    )
