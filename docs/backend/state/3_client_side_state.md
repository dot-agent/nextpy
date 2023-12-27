# Client-Side State

The state system is user-friendly and efficient. By connecting UI components to state variables, your app can respond to changes, creating a smooth user experience. Nextpy handles state management on the server side, ensuring consistent data, security, and real-time updates for multiple users and tabs.

## Unique State per User

In a Nextpy app, each user has their own independent state. This means that when different users interact with the application, their actions and resulting state changes do not interfere with each other. Here's how this works:

### How Nextpy Handles User-Specific State

When a user connects to a Nextpy application, the server generates a unique state instance for that user. This instance holds all the state variables and remains separate from the states of other users. As the user interacts with the application, their actions are transmitted to the server. The server then updates the user's specific state instance and sends the required updates back to the client's UI.

### Example: Personalized Greetings

Let's illustrate this with an example of a personalized greeting message that updates based on user input.

```python
import nextpy as xt

class GreetingState(xt.State):
    name: str = "World"  # Default greeting name

    def update_name(self, new_name: str):
        self.name = new_name  # Update the name based on user input

def greeting_input():
    return xt.input(
        placeholder="Enter your name",
        on_change=GreetingState.update_name  # Update name on input change
    )

def personalized_greeting():
    return xt.text(f"Hello, {GreetingState.name}!")  # Display personalized greeting

def index():
    return xt.vstack(
        personalized_greeting(),
        greeting_input()
    )

```

In the example above, each user can type their name into the input field, and the greeting message updates accordingly. Each user sees their own name without affecting others.

## Independent State Across Tabs

When a user opens multiple tabs of the same Nextpy application, each tab maintains an independent state. This allows users to work with different views or parts of the application simultaneously without any cross-interference.

### How Nextpy Maintains Tab Independence

We assign a unique session ID to each tab, which is used to manage state independently. Any state changes in one tab do not affect the state in other tabs, even if they belong to the same user.

### Example: Multi-Tab Counter

Consider an application with a simple counter that can be incremented by the user. If the same user opens the application in two different tabs, each tab will have its own counter state.

```python

import nextpy as xt

class CounterState(xt.State):
    count: int = 0

    def increment(self):
        self.count += 1  # Increment count for this tab's state

def counter_display():
    return xt.text(f"Count: {CounterState.count}")

def increment_button():
    return xt.button(
        "Increment",
        on_click=CounterState.increment  # Increment count on button click
    )

def index():
    return xt.vstack(
        counter_display(),
        increment_button()
    )

```

With the code above, each tab will show its own count value. Clicking the "Increment" button in one tab will not change the count displayed in another tab.

By understanding the client-side state management in Nextpy, developers can create applications that provide personalized experiences for users and respect the independence of their actions across multiple tabs. This approach to state management is powerful for building scalable and interactive web applications.
