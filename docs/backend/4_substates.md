# Substates

When building complex apps like shopping cart and checkout flow. Managing the entire state as a single unit can quickly become messy and difficult to handle. This is where substates come in!

Think of substates as separate “RAM” for each page or section. Each substate holds the data and logic specific to its area, like the items in your cart or your login credentials. This keeps your code organized and focused, making it easier to navigate and update individual functionalities without affecting the others.

Why use substates**:**

- Break down complex state into smaller, more manageable classes.
- Improve code organization and maintainability, especially in larger apps.
- Facilitate sharing of common state resources across different parts of your application.

## Create Multiple States

**To create substates, simply define separate classes that inherit from `xt.State` for each page or section.**

In a counter application, you might want to maintain different counters on separate pages. Each counter can have its own substate to manage its value independently.

### Example

```python
# home_counter.py
import nextpy as xt

class HomeCounterState(xt.State):
    """State for the counter on the home page."""
    count: int = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

def home_counter():
    return xt.vstack(
        xt.button("-", on_click=HomeCounterState.decrement),
        xt.text(HomeCounterState.count),
        xt.button("+", on_click=HomeCounterState.increment),
    )

# about_counter.py
import nextpy as xt

class AboutCounterState(xt.State):
    """State for the counter on the about page."""
    count: int = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

def about_counter():
    return xt.vstack(
        xt.button("-", on_click=AboutCounterState.decrement),
        xt.text(AboutCounterState.count),
        xt.button("+", on_click=AboutCounterState.increment),
    )

```

Each page has its own counter, managed by its respective state class.

## Accessing Substate Across Pages

You can import and access the substate classes from other modules if you need to interact with a state from a different part of your application.

### Example

```python
# main.py
import nextpy as xt
from home_counter import HomeCounterState, home_counter
from about_counter import AboutCounterState, about_counter

def index():
    return xt.vstack(
        xt.box(home_counter()),
        xt.box(about_counter()),
        xt.text(f"Total Count: {HomeCounterState.count + AboutCounterState.count}"),
    )
    
app = xt.App()
app.add_page(index)

```

In `index`, we import both `HomeCounterState` and `AboutCounterState` to display the total count from both counters combined.

## State Inheritance

**You can even create hierarchies of states for shared elements.** Think of a base state holding common variables and event handlers, like the current logged-in user. Other substates can then inherit from this base state, accessing and modifying shared information as needed.

This allows you to define common behavior or variables in a base state and extend this to more specific substates.

### Example

```python
class BaseCounterState(xt.State):
    """Base state with common counter logic."""
    count: int = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

class SpecializedCounterState(BaseCounterState):
    """A specialized counter with additional features."""
    special_feature_enabled: bool = True

    def special_increment(self):
        if self.special_feature_enabled:
            self.count += 10
        else:
            super().increment()

def specialized_counter():
    return xt.vstack(
        xt.button("-", on_click=SpecializedCounterState.decrement),
        xt.text(SpecializedCounterState.count),
        xt.button("+10", on_click=SpecializedCounterState.special_increment),
    )

def index():
    return xt.vstack(
    specialized_counter(),
    )

app = xt.App()
app.add_page(index)

```

`SpecializedCounterState` inherits from `BaseCounterState`, allowing it to use the common `increment` and `decrement` methods, as well as adding its own `special_increment` method.

By using substates and state inheritance, you can maintain a clean and organized codebase for your Nextpy applications, making them easier to develop, understand, and maintain as they grow in complexity.
