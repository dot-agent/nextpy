
# What are Components?

- Components are like building blocks for crafting a app's interface, allowing modular and reusable design elements.
- Components in Nextpy are defined using Python functions. They encapsulate React components, providing a Pythonic development experience without requiring JavaScript knowledge.
- A component can range from simple text to interactive buttons or dynamic progress bars.

## Creating Components

### Children 

- Children are elements that reside within a component. They form the content of the component and can vary from simple elements like text or images to complex nested components.
- Children are passed as positional arguments in Python. This means they are provided in the order that the component's function expects.
- Example: In `xt.text("Welcome to Nextpy")`, the string `"Welcome to Nextpy"` is the child of the `xt.text` component. It's the content that this component displays.

### Props 

- Props, short for properties, are parameters used to define and modify the behavior and style of a component. Props provide customization options for a component, influencing its appearance and functionality.
- Props are passed as keyword arguments, where each argument is specified with a keyword or parameter name.
- Example: In `xt.text("Text", color="blue")`, `color="blue"` is a keyword argument. The `color` keyword specifies the property to modify, and `"blue"` is the value assigned to that property.

- **Nesting for Complexity**: Components can be nested within one another. This hierarchical structuring enables the creation of complex user interfaces by combining simpler components.


### Example : Nested Components

- Create a layout with two circular progress indicators, demonstrating nested components.
- One displays a fixed progress value (50%), and the other an indeterminate progress.

```python
xt.hstack(
            xt.circular_progress(
                xt.circular_progress_label("⛽"),
                value=50,
            ),
            xt.circular_progress(
                xt.circular_progress_label("📶"),
                is_indeterminate=True,
            ),
        )
```

- **`xt.hstack`** arranges components horizontally.
- Each **`xt.circular_progress`** component presents a unique progress state.

## Pages in Nextpy

- Pages in Nextpy represent different sections of a website, each associated with a unique URL.
- Define a page by creating a function that returns a component and link it to a URL.

### Example: Creating Pages

```python
def index():
    return xt.text("🌌 Welcome to Intergalactic Travel! 🚀")

def about():
    return xt.text("Explore our Exotic Space Destinations ✨")

app = xt.App()
app.add_page(index, route="/")
app.add_page(about, route="/about")

```

- The **`index()`** function is linked to the root ("/") URL.
- **`about()`** is associated with the "/about" URL, directing users to the about page.

### What Are Props?

- In the world of Nextpy, props are like customizable settings for your components, offering a blend of functionality and aesthetic control.
- They're the tools you use to tailor each component's look and behavior, akin to adjusting settings on a sophisticated gadget.

**Component Specific Props**

- Just like different gadgets have unique features, each Nextpy component comes with its own set of specific props.
- Take the **`xt.avatar`** component, for example, which uses a **`name`** prop to give it a unique identity.

**Example: Creating a Unique Avatar**

```python

xt.avatar(name="Adventurer Alex")

```

- This line is akin to naming a character in a story, giving life to an avatar named "Adventurer Alex."
- For a deeper dive into each component's unique traits, explore Nextpy's comprehensive documentation.

**Style Props**

- Nextpy empowers you to apply CSS properties directly as props, merging web design's creativity with Python's power.

**Example: Stylish Button**

```python

xt.button(
    "Press Me!",
    border_radius="10px",
    box_shadow="0 5px 15px rgba(0, 0, 0, 0.3)",
    background_image="linear-gradient(45deg, #fe6b8b 30%, #ff8e53 90%)",
    color="white",
    _hover={"background": "lightgrey"}
)

```

- This snippet crafts a button that stands out, combining a sleek design with an interactive hover effect.

**HTML Props**

- Nextpy allows you to incorporate HTML-like props, adding another layer of web development familiarity to your projects.

**Example: Welcoming Box**

```python

xt.box(
    "Welcome to Nextpy!",
    id="welcome-area",
    class_name=["greet", "introduction"]
)

```

- This creates a welcoming box, complete with an ID and class names, like setting up a digital greeting area.

**Binding Props to State**

- With Nextpy's State feature, component behavior dynamically responds to app state changes.

**Example: Toggleable Badge**

```python

class DynamicState(xt.State):
    label: str = "Click to Change"
    color: str = "blue"

    def toggle_color(self):
        self.color = "green" if self.color == "blue" else "blue"

def index():
    return xt.badge(
        DynamicState.label,
        background_color=DynamicState.color,
        on_click=DynamicState.toggle_color
    )

```

- This interactive badge changes color upon clicking, demonstrating the dynamic nature of props bound to state.

**Conditional Props**

- **`xt.cond`** provides the flexibility to modify props based on conditions, much like setting up rules in a board game.

**Example: Responsive Slider**

```python

class GameLevelState(xt.State):
    level: int = 30

def level_slider():
    return xt.slider(
        on_change_end=GameLevelState.set_level,
        track_color=xt.cond(GameLevelState.level > 50, "forestgreen", "crimson")
    )

```

- This slider adjusts its track color based on the game level, adding a fun, interactive element to the user interface.
