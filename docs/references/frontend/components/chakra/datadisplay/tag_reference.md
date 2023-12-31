##  Reference for nextpy/frontend/components/chakra/datadisplay/tag(Generated by a LLM. Pending Review)

# Nextpy Documentation: Tag Component

## Tag

### Overview

The `Tag` component in Nextpy is used to create labels or keywords for items that can be used to describe properties, metadata, categories, or to filter content. Tags can be interactive, with the ability to add icons or a close button to remove the tag from the view.

### Use Cases

- Displaying a list of filters on a search page.
- Adding metadata to items such as articles, products, or images.
- Visual representation of categories or tags associated with blog posts.
- User-interface for selecting multiple items from a set of options.

### Anatomy

#### Basic Usage

```python
# Import the necessary components
from nextpy.components.chakra.datadisplay.tag import Tag

# Create a basic tag
basic_tag = Tag.create(children="Basic Tag")
```

#### Advanced Usage with Icons and Close Button

```python
# Import the necessary components
from nextpy.components.chakra.datadisplay.tag import Tag, TagLabel, TagLeftIcon, TagRightIcon, TagCloseButton

# Create an advanced tag with icons and close button
advanced_tag = Tag.create(
    children=[
        TagLeftIcon.create(icon="info"),  # Replace "info" with your icon choice
        TagLabel.create(children="Advanced Tag"),
        TagRightIcon.create(icon="check"),  # Replace "check" with your icon choice
        TagCloseButton.create()
    ],
    color_scheme="blue",  # Optional: customize the color scheme
    size="md",  # Optional: set the size
    variant="solid"  # Optional: choose the variant
)
```

### Components

#### `TagLabel`
A sub-component that defines the label within the tag.

#### `TagLeftIcon`
An optional sub-component placed before the label for adding an icon.

#### `TagRightIcon`
An optional sub-component placed after the label for adding an icon.

#### `TagCloseButton`
An optional sub-component that provides a clickable close button.

### Properties

| Prop Name        | Type                                                     | Description                                                  |
| ---------------- | -------------------------------------------------------- | ------------------------------------------------------------ |
| `left_icon`      | `Optional[Component]`                                    | A component to be used as the left icon.                     |
| `right_icon`     | `Optional[Component]`                                    | A component to be used as the right icon.                    |
| `close_button`   | `Optional[Component]`                                    | A component to be used as the close button.                  |
| `color_scheme`   | `Optional[LiteralTagColorScheme]`                        | The color scheme of the tag.                                 |
| `size`           | `Optional[LiteralTagSize]`                               | The size of the tag.                                         |
| `variant`        | `Optional[LiteralVariant]`                               | The variant style of the tag.                                |
| `style`          | `Optional[Style]`                                        | The style to be applied to the tag.                          |
| `custom_attrs`   | `Optional[Dict[str, Union[Var, str]]]`                   | Custom attributes for the tag component.                     |
| Event Handlers   | `Optional[Union[EventHandler, EventSpec, list, function, BaseVar]]` | Event handlers for the corresponding browser events. |

### Notes

- When using icons, ensure that the icon names correspond to valid icons in the Nextpy library or your custom icon set.
- `TagCloseButton` should only be used if the tag is meant to be dismissible by the user.

### Best Practices

- Use clear and concise text for `TagLabel` to improve readability.
- Limit the number of tags displayed to prevent overwhelming the user.
- Employ color schemes to categorize tags and improve visual organization.
- Leverage event handlers to add interactivity to the tags, such as removing a tag from a view when the close button is clicked.