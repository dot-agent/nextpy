# Learn State Management: Mood switcher app
![image](https://github.com/dot-agent/nextpy/assets/25473195/117a7300-8fa9-4949-8699-18c36d206d53)


Let's learn basics of state mangement by building a mood switcher app. Our app will display an emoji representing a mood. When the user clicks on the emoji, it will switch to a different mood, cycling through a predefined list of moods. Here's the final code structure:

### Complete Code Overview:

```python
import nextpy as xt

class MoodState(xt.State):
    moods: list[str] = ["😊", "😂", "🤔", "😢", "😠"]
    index: int = 0

    def next_mood(self):
        self.index = (self.index + 1) % len(self.moods)

    @xt.var
    def current_mood(self) -> str:
        # Return the emoji at the current index
        return self.moods[self.index]
    
def mood_switcher():
    return xt.text(
        MoodState.current_mood,  # Use the current_mood computed var for the emoji
        on_click=MoodState.next_mood,  # Link the click event to the next_mood method
        style={"cursor": "pointer", "font-size": "4rem"}  # Style to indicate interactivity and increase size
    )

def index():
    return xt.vstack(
        xt.text("Click the emoji to change the mood!"),
        mood_switcher(),
        spacing="20px",  # Add some spacing between elements
    )

# Add state and page to the app.
app = xt.App()
app.add_page(index)

```
## Step-by-Step Explanation

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

    @xt.var
    def current_mood(self) -> str:
        # Return the emoji at the current index
        return self.moods[self.index]

```

The `current_mood` computed var returns the emoji that corresponds to the current `index`.

### Step 4: Create the Emoji Component

Let's create a component that displays the emoji and responds to clicks:

```python
def mood_switcher():
    return xt.text(
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

The `index` function uses `vstack` to vertically stack a text prompt and our `mood_switcher` component, with added spacing for better visual separation.

### Step 6: Setting Up Our Application
Finally, initialize the app and add the index page:

```python
app = xt.App()  # Initialize the application
app.add_page(index)  # Add the index page to the application
```

### Running the Mood Switcher

Run your Nextpy app, and you'll see the Mood Switcher in action. Every click on the emoji will switch to the next one, creating a simple yet engaging interaction that demonstrates the use of state in a Nextpy application.


### Key takeaways:**

- **Stateful components:** Use state to create dynamic and interactive elements in Nextpy apps.
- **Event handlers:** Respond to user interactions and update the app's state accordingly.
- **Computed variables:** Derive values based on state, keeping components reactive to changes.


Want to dive deeper into this topic? Explore more at [Nextpy's State Introduction documentation](https://github.com/dot-agent/nextpy/blob/main/docs/backend/1_state_intro.md) on GitHub. 
