##  Reference for nextpy/frontend/components/chakra/datadisplay/badge

## Badge

### Overview
The `Badge` component is used to highlight an item's status for quick recognition. It's a label-like element that you can place in your UI to represent counts, statuses, or just to bring attention to certain elements.

### Purpose
Badges are useful for:
- Displaying counts next to inbox messages, notifications, or other similar components that indicate quantity.
- Representing status, like 'success', 'error', or 'pending', next to a task, a process, or a user input.
- Drawing attention to new or important items.

### Use Cases
- Show the number of unread messages in an email application.
- Indicate an item is on sale in an e-commerce website.
- Tag a document with a 'draft' or 'final' status in a document management system.

### Structure and Usage
The `Badge` component is flexible and can be easily integrated into various parts of an application. It is designed to be used as a child of other components or standalone.

#### Basic Usage
```python
import nextpy as xt

# Creating a simple badge with default variant
simple_badge = xt.badge("Default Badge")

# Creating a badge with the 'solid' variant and a specific color scheme
solid_badge = xt.badge("Solid Badge", variant="solid", color_scheme="green")
```

#### Advanced Usage
```python
# Using custom styles and event handlers
custom_badge = xt.badge(
    "Custom Badge",
    variant="outline",
    color_scheme="purple",
    style=Style(margin="10px", padding="5px"),
    on_click=lambda event: print("Badge clicked!")
)
```

### Components
The `badge` component has the following properties:

| Prop Name      | Type                                            | Description                                                         |
| -------------- | ----------------------------------------------- | ------------------------------------------------------------------- |
| `variant`      | `Literal["solid", "subtle", "outline"]` or `Var`| The visual style variant of the badge.                              |
| `color_scheme` | `str` or `Var`                                  | Predefined color schemes for the badge, e.g., 'blue', 'red', etc.   |
| `style`        | `Style`                                         | Custom styles to be applied to the badge.                           |
| `on_click`     | `EventHandler` or `EventSpec`                   | Event handler that is called when the badge is clicked.             |

### Notes
- When using variables (`Var`) for `variant` and `color_scheme`, ensure that the variable type matches the expected input type.
- Custom attributes (`custom_attrs`) can be used to add non-standard attributes to the component.

### Best Practices
- Use clear and concise text for badges to ensure they are legible.
- Choose the `variant` and `color_scheme` that best fit the context of the badge in your application to provide the most effective visual cues to users.
- For event handling, like `on_click`, ensure that the functionality enhances the user experience and is not disruptive.
