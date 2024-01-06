# State Basics

Let's use a simple counter example to see how you define, manage, and interact with state

## Defining a State Class

In Nextpy, state is defined by creating a class that inherits from `xt.State`. This class serves as the structure for the dynamic data your application will manage.

Here's a simple example of defining a state class:

```python
import nextpy as xt

class CounterState(xt.State):
    # A base var to keep track of the count
    count: int = 0

```

In the example above, `CounterState` is our state class, and it has one base var called `count`, initialized to 0.

## Base Vars and Computed Vars

Vars are the variables that store the changeable data in your state class. Let's examine the two types of vars with examples:

### Base Var

Base vars hold the primary data for your application. They are directly modifiable by event handlers. For instance, in a counter app, the base var would be the counter value itself.

```python
class CounterState(xt.State):
    count: int = 0  # This is a base var representing the counter value

```

### Computed Var

Computed vars are derived from base vars and are recalculated automatically when the base vars change. Here's how you can define a computed var that toggles a message based on the count:

```python
class CounterState(xt.State):
    count: int = 0

    @xt.var
    def message(self) -> str:
        # This is a computed var that returns a message based on the count
        return "Even" if self.count % 2 == 0 else "Odd"

```

## Event Triggers and Handlers

Event triggers are linked to user actions like clicking a button, while event handlers are functions that respond to these triggers by updating the state.

Here's an example of an event handler that increments the counter:

```python
class CounterState(xt.State):
    count: int = 0

    def increment(self):
    # Event handler that increments the count
        self.count += 1

```

Now, let's link this event handler to an event trigger using a button component:

```python
def index():
    return xt.button(
        "Increment",
        on_click=CounterState.increment,  # Linking the button click to the increment event handler
    )

```

With the setup above, clicking the "Increment" button will trigger the `increment` event handler, updating the `count` base var and causing Nextpy to re-render the relevant components.

# Working with State

Now that we've covered the basics, let's put everything together to see how state operates within a complete example.

## Creating and Initializing State

When your Nextpy app starts, it automatically initializes the state as defined by your state class. Here's a simple counter app that sets up the initial state:

```python
# state.py
import nextpy as xt

class CounterState(xt.State):
    count: int = 0

```

## Connecting Events to Handlers

Next, we connect our event triggers to the appropriate event handlers:

```python
# components.py
import nextpy as xt
from state import CounterState

def increment_button():
    return xt.button(
        "Increment",
        on_click=CounterState.increment
    )

```

In the code snippet above, the `on_click` property of the button is connected to the `increment` method of our `CounterState` class.

## Modifying State in Handlers

The `increment` method modifies the state each time it's called by a user action:

```python
# state.py
import nextpy as xt

class CounterState(xt.State):
    count: int = 0

    def increment(self):
        self.count += 1

```

Each time the button is clicked, `increment` is executed, and `count` is increased by one.

## Re-rendering Components

Finally, let's display the counter value and ensure it updates when the state changes:

```python
# components.py
import nextpy as xt
from state import CounterState

def counter_display():
    return xt.text(f"Current count: {CounterState.count}")

def index():
    return xt.vstack(
        counter_display(),
        increment_button()
    )

```

The `counter_display` function creates a text component that shows the current count. The `index` function arranges the display and button vertically using `vstack`. When `count` changes, Nextpy automatically re-renders the `text` component to reflect the new value.

By following the steps outlined in this tutorial, you can create interactive components that respond to user inputs and manage state efficiently in your Nextpy applications.
