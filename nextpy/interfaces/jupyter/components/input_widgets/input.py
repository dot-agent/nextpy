from typing import Any, Callable, Optional, TypeVar, Union, cast, overload, List, Dict

import ipyvue
import ipyvuetify as vw
import reacton
from typing_extensions import Literal

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.alias import rv as v

T = TypeVar("T")


@widget.component
def input(
    label: str = '',
    value: Union[str, widget.Reactive[str]] = "",
    on_value: Callable[[str], None] = None,
    disabled: bool = False,
    password: bool = False,
    continuous_update: bool = False,
    update_events: List[str] = ["blur", "keyup.enter"],
    error: Union[bool, str] = False,
    message: Optional[str] = None,
    class_name: str = '',
    style: str = ''
):
    """Free form text input.

    ### Basic example:

    ```widget
    import nextpy.interfaces.jupyter

    text = widget.reactive("Hello world!")
    continuous_update = widget.reactive(True)

    @widget.component
    def Page():
        widget.Checkbox(label="Continuous update", value=continuous_update)
        widget.InputText("Enter some text", value=text, continuous_update=continuous_update.value)
        with widget.row():
            widget.button("Clear", on_click=lambda: text.set(""))
            widget.button("Reset", on_click=lambda: text.set("Hello world"))
        widget.Markdown(f"**You entered**: {text.value}")
    ```

    ### Password input:

    This will not show the entered text.

    ```widget
    import nextpy.interfaces.jupyter

    password = widget.reactive("Super secret")
    continuous_update = widget.reactive(True)

    @widget.component
    def Page():
        widget.Checkbox(label="Continuous update", value=continuous_update)
        widget.InputText("Enter a passsword", value=password, continuous_update=continuous_update.value, password=True)
        with widget.row():
            widget.button("Clear", on_click=lambda: password.set(""))
            widget.button("Reset", on_click=lambda: password.set("Super secret"))
        widget.Markdown(f"**You entered**: {password.value}")
    ```


    ## Arguments

    * `label`: Label to display next to the slider.
    * `value`: The currently entered value.
    * `on_value`: Callback to call when the value changes.
    * `disabled`: Whether the input is disabled.
    * `password`: Whether the input is a password input (typically shows input text obscured with an asterisk).
    * `continuous_update`: Whether to call the `on_value` callback on every change or only when the input loses focus or the enter key is pressed.
    * `update_events`: A list of events that should trigger `on_value`. If continuous update is enabled, this will effectively be ignored,
        since updates will happen every change.
    * `error`: If truthy, show the input as having an error (in red). If a string is passed, it will be shown as the error message.
    * `message`: Message to show below the input. If `error` is a string, this will be ignored.
    * `classes`: List of CSS classes to apply to the input.
    * `style`: CSS style to apply to the input.
    """
    reactive_value = widget.use_reactive(value, on_value)
    del value, on_value

    def set_value_cast(value):
        reactive_value.value = str(value)

    def on_v_model(value):
        if continuous_update:
            set_value_cast(value)

    messages = []
    if error and isinstance(error, str):
        messages.append(error)
    elif message:
        messages.append(message)
    text_field = v.TextField(
        v_model=reactive_value.value,
        on_v_model=on_v_model,
        label=label,
        disabled=disabled,
        type="password" if password else None,
        error=bool(error),
        messages=messages,
        class_=class_name,
        style_=style,
    )
    use_change(text_field, set_value_cast, enabled=not continuous_update, update_events=update_events)
    return text_field


def use_change(el: reacton.core.Element, on_value: Callable[[Any], Any], enabled=True, update_events=["blur", "keyup.enter"]):
    """Trigger a callback when a blur events occurs or the enter key is pressed."""
    on_value_ref = widget.use_ref(on_value)
    on_value_ref.current = on_value

    def add_events():
        def on_change(widget, event, data):
            if enabled:
                on_value_ref.current(widget.v_model)

        import nextpy.interfaces.jupyter as widget
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
