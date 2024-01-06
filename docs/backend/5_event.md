# Event

In Nextpy, events are like **mini-earthquakes** that shake your app when users interact with it. For example, clicking a button, typing in a box, or hovering over something can all trigger events.

These events are like **signals to your app** saying, "Hey, something just happened!" Then, your app can react to these signals using **event handlers**, which are like **tiny firefighters** rushing to the scene to put out the "fire" (update the app based on the event).

Here's the breakdown:

- **Event:** Something a user does (click, type, etc.)
- **Event handler:** A function that reacts to the event
- **Result:** The app updates itself based on the handler's instructions

So, events are how users **talk to your app**, and event handlers are how your app **listens and responds**. They're the building blocks of making your app interactive and dynamic!

Here are some cool things events can do:

- Change the text or color of something
- Show or hide elements
- Run calculations or fetch data
- Basically, anything you can imagine to make your app more fun and responsive!

## Event Triggers

Event triggers are properties that you can attach to components to listen for user actions. When a user performs the specified action, the associated event handler is called.

Think of event triggers as special antennas built into each component of your app.

- These antennas are always listening for specific user actions, like clicking, hovering, typing, or form submissions.
- When a user interacts with a component in a way that matches an antenna's listening pattern, it catches the signal and sends an alert to the app's brain (the event handler).
- The event handler then takes over, processing the alert and deciding what changes to make to the app's state and UI in response.

### Counter Example

```python
import nextpy as xt

class CounterState(xt.State):
    count: int = 0

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

def index():
    return xt.vstack(
        xt.button("-", on_click=CounterState.decrement),
        xt.text(CounterState.count),
        xt.button("+", on_click=CounterState.increment),
    )

app = xt.App()
app.add_page(index)
```

In this counter example, clicking the "+" and "-" buttons triggers the `increment` and `decrement` event handlers, respectively, updating the `count`.

Key points:

- Depends on **components:** Every component has its own collection of triggers, defining the types of actions it can listen for.
- **Common examples:** Some frequently used triggers include `on_click`, `on_change`, `on_submit`, and `on_mouse_over`.

## Event Arguments

In some situations, you'll want to provide extra information to event handlers when they're triggered. This is where event arguments come in.

To send specific data to an event handler, you'll use a lambda function as a bridge between the event trigger and the handler. Here's how it works:

1. Imagine a button with an `on_click` trigger.
2. Instead of directly linking it to the event handler, you'll create a lambda function as a middleman.
3. This lambda function will hold the arguments you want to pass to the handler.
4. When the button is clicked, the lambda function executes, calling the event handler with those arguments.

### Counter Example with Step Size

```python
import nextpy as xt

class CounterState(xt.State):
    count: int = 0

    def change_count(self, step: int):
        self.count += step

def index():
    return xt.vstack(
        xt.button("-", on_click=lambda: CounterState.change_count(-1)),
        xt.text(CounterState.count),
        xt.button("+", on_click=lambda: CounterState.change_count(1)),
    )

```

Here, we use a lambda function to pass a step size to the `change_count` handler when a button is clicked.

## Setters

Think of setters as express delivery services for your base variables. They offer a quick and efficient way to update values without the need for custom handlers, making your code cleaner and more readable.

Here's how they work:

1. Imagine each base variable having a dedicated delivery service (setter) ready to go.
2. To use a setter, just call its name, along with the new value you want to deliver.
3. The setter immediately updates the variable with the new value, triggering a UI refresh to reflect the change.

### Setter example

```python
import nextpy as xt

class CounterState(xt.State):
    count: int = 0

def index():
    return xt.vstack(
        xt.button("Reset", on_click=CounterState.set_count(0)),
        xt.text(CounterState.count),
        xt.button("+", on_click=lambda: CounterState.set_count(CounterState.count + 1)),
    )

```

The "Reset" button uses the `set_count` setter to reset the count to 0.

**Key Points:**

- **Specific to base variables:** Setters are not available for computed vars, which rely on formulas for updates.
- **Simple updates:** Ideal for straightforward value changes. For more complex logic or interactions, consider custom event handlers.

---

## Advanced Event Handlers

Beyond the basics, advanced techniques like yielding multiple updates, chaining event handlers, and returning events to create complex workflows and sequences of actions with ease.

### Yielding Multiple Updates

In Nextpy, event handlers typically update the UI once they complete their execution. However, for more interactive and responsive UIs, you can yield multiple updates from within an event handler. This approach is particularly useful for operations that take time, like data processing or loading content.

**How It Works:**

1. **Use of `yield`:** Inside the event handler, use the `yield` keyword to pause execution and send a current state update to the UI.
2. **Triggering State Updates:** Each `yield` triggers a `StateUpdate`, refreshing the UI with the latest state changes.

**Common Use Cases:**

- **Displaying Loading Indicators:** Show progress or loading indicators during lengthy tasks.
- **Multi-Step Processes:** Visualize steps in a process, enhancing user experience.
- **Real-Time Feedback:** Update elements like progress bars or animations in real-time.

### Example: Counter with Timed Increment

```python
import asyncio
import nextpy as xt

class CounterState(xt.State):
    count: int = 0

    async def timed_increment(self):
        for _ in range(5):
            await asyncio.sleep(1)
            self.count += 1
            yield

def index():
    return xt.vstack(
        xt.text(CounterState.count),
        xt.button("Increment Over 5 Seconds", on_click=CounterState.timed_increment),
    )

```

**Asynchronous Compatibility:** This feature integrates seamlessly with asynchronous operations, maintaining responsiveness during waiting tasks.

### Calling Handlers from Handlers

Nextpy allows event handlers to trigger other event handlers. This approach is excellent for breaking down complex tasks into manageable functions, enhancing code organization and reusability.

**How It Works:**

1. **Handler Calls:** Use `self.call_handler` within an event handler to invoke another handler by name.
2. **State Modification:** The called handler executes, potentially altering the application state.
3. **Control Return:** Control returns to the original handler after the called handler completes.
4. **Incremental Updates:** Use `yield` in both handlers for smoother, incremental UI updates.

### Example: Countdown Sequence

```python
import asyncio
import nextpy as xt

class CounterState(xt.State):
    count: int = 0

    def start_sequence(self):
        self.set_count(10)  # Initialize count
        return CounterState.decrement_sequence  # Return class method

    @xt.background 
    async def decrement_sequence(self):
        while self.count > 0:
            await asyncio.sleep(1)
            async with self:  # Required for state modification in background tasks
                self.count -= 1
            yield  # Yield to send the update to the frontend

def index():
    return xt.vstack(
        xt.text(CounterState.count),
        xt.button("Start Countdown", on_click=CounterState.start_sequence),
    )

```

**Note:** You should use the @xt.background decorator on an asynchronous method within your state class 2. Since your decrement_sequence function is designed to update the state over time, it should be marked as a background task and it should be an asynchronous method.
**Note:** Clicking "Start Countdown" initializes the counter to 10 and triggers a countdown.

### Returning Events from Handlers

Event handlers in Nextpy can also trigger new events, creating a chain of actions. This feature is crucial for designing complex interactions where one action leads to another.

**How It Works:**

1. **Event Scheduling:** Handlers can return the name of another event handler, scheduling it for execution.
2. **Controlled Sequences:** This creates an ordered sequence of tasks, ensuring actions occur as planned.
3. **Immediate UI Updates:** Even when the current handler is busy, UI updates happen immediately.
4. **Class Name Usage:** Use the class or substate name to return events, not `self`.

```python
import nextpy as xt

class TaskQueueState(xt.State):
    current_task: int = 0
    total_tasks: int = 5

    def complete_task(self):
        if self.current_task < self.total_tasks:
            self.current_task += 1
            # Return the name of this handler to trigger it again
            return TaskQueueState.check_next_task
        # No more tasks to complete
        return None

    def check_next_task(self):
        # This function could be used to check the condition to continue the task
        if self.current_task < self.total_tasks:
            # If there are more tasks, complete the next task
            return TaskQueueState.complete_task
        # All tasks are completed
        self.current_task = 0  # Reset the task queue

def index():
    return xt.vstack(
        xt.text(f"Current Task: {TaskQueueState.current_task}"),
        xt.button("Complete Task", on_click=TaskQueueState.complete_task),
        xt.text(f"Total Tasks: {TaskQueueState.total_tasks}")
    )


```

## Special Events

Nextpy supports special events like alerts, which can interact with the browser.

### Counter Example with Alert

```python
import nextpy as xt

class CounterState(xt.State):
    count: int = 0

    def increment_and_alert(self):
        self.count += 1
        if self.count == 5:
            return xt.window_alert("Counter reached 5!")

def index():
    return xt.vstack(
        xt.text(CounterState.count),
        xt.button("+", on_click=CounterState.increment_and_alert),
    )

```

The "+" button increments the counter, and when it reaches 5, a browser alert is triggered.
