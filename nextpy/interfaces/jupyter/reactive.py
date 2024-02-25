from typing import TypeVar

from nextpy.interfaces.jupyter.toestand import Reactive

__all__ = ["reactive", "Reactive"]

T = TypeVar("T")


def reactive(value: T) -> Reactive[T]:
    """Creates a new Reactive object with the given initial value.

    Reactive objects are mostly used to manage global or application-wide state in
    Solara web applications. They provide an easy-to-use mechanism for keeping
    track of the changing state of data and for propagating those changes to
    the appropriate UI components. For managing local or component-specific
    state, consider using the [`widget.use_state()`](/api/use_state) function.


    Reactive variables can be accessed using the `.value` attribute. To modify
    the value, you can either set the `.value` property directly or use the
    `.set()` method. While both approaches are equivalent, the `.set()` method
    is particularly useful when you need to pass it as a callback function to
    other components, such as a slider's `on_value` callback.

    When a component uses a reactive variable, it
    automatically listens for changes to the variable's value. If the value
    changes, the component will automatically re-render to reflect the updated
    state, without the need to explicitly subscribe to the variable.

    Reactive objects in Solara are also context-aware, meaning that they can
    maintain separate values for each browser tab or user session. This enables
    each user to have their own independent state, allowing them to interact
    with the web application without affecting the state of other users.

    Args:
        value (T): The initial value of the reactive variable.

    Returns:
        Reactive[T]: A new Reactive object with the specified initial value.

    Example:

    ```python
    >>> counter = widget.reactive(0)
    >>> counter.value
    0
    >>> counter.set(1)
    >>> counter.value
    1
    >>> counter.value += 1
    >>> counter.value
    2
    ```


    ## Solara example

    Here's an example that demonstrates the use of reactive variables in Solara components:

    ```widget
    import nextpy.interfaces.jupyter

    counter = widget.reactive(0)

    def increment():
        counter.value += 1


    @widget.component
    def CounterDisplay():
        widget.Info(f"Counter: {counter.value}")


    @widget.component
    def IncrementButton():

        widget.button("Increment", on_click=increment)


    @widget.component
    def Page():
        IncrementButton()
        CounterDisplay()
    ```

    In this example, we create a reactive variable counter with an initial value of 0.
    We define two components: `CounterDisplay` and `IncrementButton`. `CounterDisplay` renders the current value of counter,
    while `IncrementButton` increments the value of counter when clicked.
    Whenever the counter value changes, `CounterDisplay` automatically updates to display the new value.

    """
    return Reactive(value)
