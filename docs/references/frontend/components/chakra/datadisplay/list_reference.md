##  Reference for nextpy/frontend/components/chakra/datadisplay/list(Generated by a LLM. Pending Review)

# Nextpy List Component Documentation

## Overview

The Nextpy framework provides a set of components for creating and managing lists in a full-stack Python application. These components are designed to work with the Chakra UI library, providing a consistent look and feel along with extensive customization options.

## Anatomy

The Nextpy list components allow you to create ordered and unordered lists, as well as individual list items. The main components include:

- `List`: The base list component from which ordered and unordered lists are derived.
- `ListItem`: An individual item within a list.
- `OrderedList`: A list component that displays its items in a numbered format.
- `UnorderedList`: A list component that displays its items with bullet points.

### Basic Usage

To create a basic unordered list:

```python
from nextpy.components.chakra.datadisplay.list import UnorderedList, ListItem

unordered_list = UnorderedList.create(
    ListItem.create("First item"),
    ListItem.create("Second item"),
    ListItem.create("Third item")
)
```

To create a basic ordered list:

```python
from nextpy.components.chakra.datadisplay.list import OrderedList, ListItem

ordered_list = OrderedList.create(
    ListItem.create("First item"),
    ListItem.create("Second item"),
    ListItem.create("Third item")
)
```

### Advanced Usage

For more advanced scenarios, you can use the `items` prop with dynamic data and include custom styling:

```python
from nextpy.components.chakra.datadisplay.list import UnorderedList, ListItem
from nextpy.backend.vars import Var

# Dynamic list of items
items_var = Var(["Apples", "Oranges", "Bananas"])

# Custom styles
custom_style = {"color": "blue", "fontWeight": "bold"}

unordered_list = UnorderedList.create(
    items=items_var,
    style_position="inside",
    style_type="disc",
    style=custom_style
)
```

## Components

### List

The base component for creating lists.

#### Properties

| Prop Name      | Type                                       | Description                                     |
| -------------- | ------------------------------------------ | ----------------------------------------------- |
| items          | Optional[list \| Var[list] \| None]        | A list of items to display in the list.         |
| spacing        | Optional[Union[Var[str], str]]             | The space between each list item.               |
| style_position | Optional[Union[Var[str], str]]             | Shorthand prop for listStylePosition.           |
| style_type     | Optional[Union[Var[str], str]]             | Shorthand prop for listStyleType.               |
| style          | Optional[Style]                            | The style of the component.                      |
| ...            |                                            | Event handlers and other standard props.        |

### ListItem

An individual item within a list.

#### Properties

| Prop Name      | Type                                       | Description                                     |
| -------------- | ------------------------------------------ | ----------------------------------------------- |
| style          | Optional[Style]                            | The style of the component.                      |
| ...            |                                            | Event handlers and other standard props.        |

### OrderedList

A component that displays its items in a numbered format. Inherits all properties from `List`.

### UnorderedList

A component that displays its items with bullet points. Inherits all properties from `List`.

## Notes

- Event handlers can be attached to list items for actions such as clicks, mouse events, and focus events.
- The `items` prop can be a static list or a `Var[list]` for dynamic content.
- Custom attributes can be passed via the `custom_attrs` prop.

## Best Practices

- Use `OrderedList` or `UnorderedList` for semantic clarity and accessibility considerations.
- Utilize `spacing`, `style_position`, and `style_type` for visual customization without additional CSS.
- Apply `style` prop judiciously, maintaining the overall design consistency.
- Bind event handlers to `ListItem` components for interactive list items.

The documentation outlined above provides a comprehensive guide for developers to effectively utilize the Nextpy list components in their web applications.