from typing import Callable, Optional, TypeVar, Union

import nextpy.interfaces.jupyter as widget

T = TypeVar("T")


def use_reactive(
    value: Union[T, widget.Reactive[T]],
    on_change: Optional[Callable[[T], None]] = None,
) -> widget.Reactive[T]:
    """Creates a reactive variable with the a local component scope.

    It is a useful alternative to `use_state` when you want to use a
    reactive variable for the component state.
    See also [our documentation on state management](/docs/fundamentals/state-management).

    If the variable passed is a reactive variable, it will be returned instead and no
    new reactive variable will be created. This is useful for implementing component
    that accept either a reactive variable or a normal value along with an optional `on_change`
    callback.

    ## Arguments:

     * value (Union[T, widget.Reactive[T]]): The value of the
            reactive variable. If a reactive variable is provided, it will be
            used directly. Otherwise, a new reactive variable will be created
            with the provided initial value. If the argument passed changes
            the reactive variable will be updated.

     * on_change (Optional[Callable[[T], None]]): An optional callback function
            that will be called when the reactive variable's value changes.

    Returns:
        widget.Reactive[T]: A reactive variable with the specified initial value
            or the provided reactive variable.

    ## Examples

    ### Replacement for use_state
    ```widget
    import nextpy.interfaces.jupyter

    @widget.component
    def ReusableComponent():
        color = widget.use_reactive("red")  # another possibility
        widget.Select(label="Color",values=["red", "green", "blue", "orange"],
                    value=color)
        widget.Markdown("### Solara is awesome", style={"color": color.value})

    @widget.component
    def Page():
        # this component is used twice, but each instance has its own state
        ReusableComponent()
        ReusableComponent()

    ```

    ### Flexible arguments

    The `MyComponent` component can be passed a reactive variable or a normal
    Python variable and a `on_value` callback.

    ```python
    import nextpy.interfaces.jupyter
    from typing import Union, Optional, Callable

    @widget.component
    def MyComponent(value: Union[T, widget.Reactive[T]],
                    on_value: Optional[Callable[[T], None]] = None,
        ):
        reactive_value = widget.use_reactive(value, on_value)
        # Use the `reactive_value` in the component
    ```
    """

    try:
        on_change_ref = widget.use_ref(on_change)
    except RuntimeError as e:
        raise RuntimeError(
            "use_reactive must be called from a component function, inside the render function.\n"
            "Do not call it top level, use [widget.reactive()](https://widget.dev/api/reactive) instead."
        ) from e
    on_change_ref.current = on_change

    def create():
        if not isinstance(value, widget.Reactive):
            return widget.reactive(value)

    reactive_value = widget.use_memo(create, dependencies=[])
    if isinstance(value, widget.Reactive):
        reactive_value = value
    assert reactive_value is not None
    updating = widget.use_ref(False)

    def forward_on_change():
        def forward(value):
            if on_change_ref.current and not updating.current:
                on_change_ref.current(value)

        return reactive_value.subscribe(forward)

    def update():
        updating.current = True
        try:
            if not isinstance(value, widget.Reactive):
                reactive_value.value = value
        finally:
            updating.current = False

    widget.use_memo(update, [value])
    # if value is a reactive variable, and it changes, we need to subscribe to the latest
    # reactive variable, otherwise we only link to it once
    widget.use_effect(forward_on_change, [value] if isinstance(value, widget.Reactive) else [])

    return reactive_value
