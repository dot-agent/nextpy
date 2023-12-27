# Learn State Management: Mood switcher app

Let's create a fun and interactive example with Nextpy—a "Mood Switcher" that changes emoji expressions based on user clicks.

## Interactive Mood Switcher Example

Our objective is to display an emoji representing a mood. When the user clicks on the emoji, it will switch to a different mood, cycling through a predefined list of moods.

### Step 1: Define the State Class

First, we'll set up our state class to keep track of the current mood:

```python
import nextpy as xt

class MoodState(xt.State):
    # A list of emojis to represent different moods
    moods: list[str] = ["😊", "😂", "🤔", "😢", "😠"]
    # The current index in the moods list
    index: int = 0

```

In `MoodState`, `moods` is a list of emoji characters, and `index` is the index of the current mood in that list.

### Step 2: Define the Event Handler

We need an event handler that updates the `index` to the next mood upon clicking the emoji:

```python
class MoodState(xt.State):
    moods: list[str] = ["😊", "😂", "🤔", "😢", "😠"]
    index: int = 0

    def next_mood(self):
        # Cycle to the next mood in the list
        self.index = (self.index + 1) % len(self.moods)

```

The `next_mood` method increments the `index` and loops back to the start once it reaches the end.

### Step 3: Create a Computed Var

Next, let's add a computed var that gives us the current mood emoji:

```python
class MoodState(xt.State):
    moods: list[str] = ["😊", "😂", "🤔", "😢", "😠"]
    index: int = 0

    def next_mood(self):
        self.index = (self.index + 1) % len(self.moods)

    @property
    def current_mood(self) -> str:
        # Return the emoji at the current index
        return self.moods[self.index]

```

The `current_mood` computed var returns the emoji that corresponds to the current `index`.

### Step 4: Create the Emoji Component

Let's create a component that displays the emoji and responds to clicks:

```python
def mood_switcher():
    return xt.Text(
        MoodState.current_mood,  # Use the current_mood computed var for the emoji
        on_click=MoodState.next_mood,  # Link the click event to the next_mood method
        style={"cursor": "pointer", "font-size": "4rem"}  # Style to indicate interactivity and increase size
    )

```

The `mood_switcher` function returns a `Text` component displaying the current mood emoji. It responds to click events by calling the `next_mood` method, and the styling changes the cursor and font size to enhance the user experience.

### Step 5: Assemble the Web Page

We assemble the page with a function that Nextpy will call to render the content:

```python
def index():
    return xt.vstack(
        xt.text("Click the emoji to change the mood!"),
        mood_switcher(),
        spacing="20px",  # Add some spacing between elements
    )

```

The `index` function uses `VStack` to vertically stack a text prompt and our `mood_switcher` component, with added spacing for better visual separation.

### Running the Mood Switcher

Run your Nextpy app, and you'll see the Mood Switcher in action. Every click on the emoji will switch to the next one, creating a simple yet engaging interaction that demonstrates the use of state in a Nextpy application.

This Mood Switcher example showcases how stateful components can be used to create interactive and playful elements in your web applications. The same principles can be applied to develop a wide range of dynamic user interfaces with Nextpy.
