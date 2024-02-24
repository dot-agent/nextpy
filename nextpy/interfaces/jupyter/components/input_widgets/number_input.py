from typing import Any, Callable, Optional, TypeVar, Union, cast, overload, List, Dict

import ipyvue
import ipyvuetify as vw
import reacton
from typing_extensions import Literal

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.alias import rv as v

T = TypeVar("T")

@widget.component
def input_float(
    label: str,
    value: Union[None, float, widget.Reactive[float], widget.Reactive[Optional[float]]] = 0,
    on_value: Union[None, Callable[[Optional[float]], None], Callable[[float], None]] = None,
    disabled: bool = False,
    optional: bool = False,
    continuous_update: bool = False,
    clearable: bool = False,
    class_name : str = '',
    style: str = ''
):
    """Numeric input (floats).

    Basic example:

    ```widget
    import nextpy.interfaces.jupyter

    float_value = widget.reactive(42.0)
    continuous_update = widget.reactive(True)

    @widget.component
    def Page():
        widget.Checkbox(label="Continuous update", value=continuous_update)
        widget.InputFloat("Enter a float number", value=float_value, continuous_update=continuous_update.value)
        with widget.row():
            widget.button("Clear", on_click=lambda: float_value.set(42.0))
        widget.Markdown(f"**You entered**: {float_value.value}")
    ```


    ## Arguments

    * `label`: Label to display next to the slider.
    * `value`: The currently entered value.
    * `on_value`: Callback to call when the value changes.
    * `disabled`: Whether the input is disabled.
    * `optional`: Whether the value can be None.
    * `continuous_update`: Whether to call the `on_value` callback on every change or only when the input loses focus or the enter key is pressed.
    * `clearable`: Whether the input can be cleared.
    * `classes`: List of CSS classes to apply to the input.
    * `style`: CSS style to apply to the input.

    """

    def str_to_float(value: Optional[str]):
        if value:
            try:
                value = value.replace(",", ".")
                return float(value)
            except ValueError:
                raise ValueError("Value must be a number")
        else:
            if optional:
                return None
            else:
                raise ValueError("Value cannot be empty")

    return _InputNumeric(
        str_to_float,
        label=label,
        value=value,
        on_value=on_value,
        disabled=disabled,
        continuous_update=continuous_update,
        clearable=clearable,
        classes=class_name,
        style=style,
    )


@widget.component
def input_int(
    label: str,
    value: Union[None, int, widget.Reactive[int], widget.Reactive[Optional[int]]] = 0,
    on_value: Union[None, Callable[[Optional[int]], None], Callable[[int], None]] = None,
    disabled: bool = False,
    optional: bool = False,
    continuous_update: bool = False,
    clearable: bool = False,
    classes: List[str] = [],
    style: Optional[Union[str, Dict[str, str]]] = None,
):
    """Numeric input (integers).

    Basic example:

    ```widget
    import nextpy.interfaces.jupyter

    int_value = widget.reactive(42)
    continuous_update = widget.reactive(True)

    @widget.component
    def Page():
        widget.Checkbox(label="Continuous update", value=continuous_update)
        widget.InputInt("Enter an integer number", value=int_value, continuous_update=continuous_update.value)
        with widget.row():
            widget.button("Clear", on_click=lambda: int_value.set(42))
        widget.Markdown(f"**You entered**: {int_value.value}")
    ```

    ## Arguments

    * `label`: Label to display next to the slider.
    * `value`: The currently entered value.
    * `on_value`: Callback to call when the value changes.
    * `disabled`: Whether the input is disabled.
    * `optional`: Whether the value can be None.
    * `continuous_update`: Whether to call the `on_value` callback on every change or only when the input loses focus or the enter key is pressed.
    * `clearable`: Whether the input can be cleared.
    * `classes`: List of CSS classes to apply to the input.
    * `style`: CSS style to apply to the input.
    """

    def str_to_int(value: Optional[str]):
        if value:
            try:
                return int(value)
            except ValueError:
                raise ValueError("Value must be an integer")
        else:
            if optional:
                return None
            else:
                raise ValueError("Value cannot be empty")

    return _InputNumeric(
        str_to_int,
        label=label,
        value=value,
        on_value=on_value,
        disabled=disabled,
        continuous_update=continuous_update,
        clearable=clearable,
        classes=classes,
        style=style,
    )


def _use_input_type(
    input_value: Union[None, T, widget.Reactive[Optional[T]], widget.Reactive[T]],
    parse: Callable[[Optional[str]], T],
    stringify: Callable[[Optional[T]], str],
    on_value: Union[None, Callable[[Optional[T]], None], Callable[[T], None]] = None,
):
    reactive_value = widget.use_reactive(input_value, on_value)  # type: ignore
    del input_value, on_value
    string_value, set_string_value = widget.use_state(stringify(reactive_value.value) if reactive_value.value is not None else None)
    # Use a ref to make sure sync_back_input_value() does not get a stale string_value
    string_value_ref = widget.use_ref(string_value)
    string_value_ref.current = string_value

    error_message = cast(Union[str, None], None)

    try:
        reactive_value.set(parse(string_value))
    except ValueError as e:
        error_message = str(e.args[0])

    def sync_back_input_value():
        def on_external_value_change(new_value: Optional[T]):
            new_string_value = stringify(new_value)
            try:
                parse(string_value_ref.current)
            except ValueError:
                # String value could be invalid when external value is changed by a different component
                set_string_value(new_string_value)
            else:
                if new_value != parse(string_value_ref.current):
                    set_string_value(new_string_value)

        return reactive_value.subscribe(on_external_value_change)

    widget.use_effect(sync_back_input_value, [reactive_value])

    return string_value, error_message, set_string_value


@widget.component
def _InputNumeric(
    str_to_numeric: Callable[[Optional[str]], T],
    label: str,
    value: Union[None, T, widget.Reactive[Optional[T]], widget.Reactive[T]],
    on_value: Union[None, Callable[[Optional[T]], None], Callable[[T], None]] = None,
    disabled: bool = False,
    continuous_update: bool = False,
    clearable: bool = False,
    class_name: List[str] = [],
    style: Optional[Union[str, Dict[str, str]]] = None,
):
    """Numeric input.

    ## Arguments

    * `label`: Label to display next to the slider.
    * `value`: The currently entered value.
    * `on_value`: Callback to call when the value changes.
    * `disabled`: Whether the input is disabled.
    * `continuous_update`: Whether to call the `on_value` callback on every change or only when the input loses focus or the enter key is pressed.
    * `classes`: List of CSS classes to apply to the input.
    * `style`: CSS style to apply to the input.
    """

    internal_value, error, set_value_cast = _use_input_type(
        value,
        str_to_numeric,
        str,
        on_value,
    )

    def on_v_model(value):
        if continuous_update:
            set_value_cast(value)

    if error:
        label += f" ({error})"
    text_field = v.TextField(
        v_model=internal_value,
        on_v_model=on_v_model,
        label=label,
        disabled=disabled,
        # we are not using the number type, since we cannot validate invalid input
        # see https://stackoverflow.blog/2022/12/26/why-the-number-input-is-the-worst-input/
        # type="number",
        hide_details=True,
        clearable=clearable,
        error=bool(error),
        class_=class_name,
        style_=style,
    )
    use_change(text_field, set_value_cast, enabled=not continuous_update)
    return text_field


def use_change(el: reacton.core.Element, on_value: Callable[[Any], Any], enabled=True, update_events=["blur", "keyup.enter"]):
    """Trigger a callback when a blur events occurs or the enter key is pressed."""
    on_value_ref = widget.use_ref(on_value)
    on_value_ref.current = on_value

    def add_events():
        def on_change(widget, event, data):
            if enabled:
                on_value_ref.current(widget.v_model)

        widget = cast(ipyvue.VueWidget, widget.get_widget(el))
        if enabled:
            for event in update_events:
                widget.on_event(event, on_change)

        def cleanup():
            if enabled:
                for event in update_events:
                    widget.on_event(event, on_change, remove=True)

        return cleanup

    widget.use_effect(add_events, [enabled])