##  Reference for nextpy/frontend/components/chakra/typography/highlight(Generated by a LLM. Pending Review)

# Nextpy Documentation: Highlight Component

## Overview

The `Highlight` component in Nextpy's Chakra UI extension is designed to visually highlight text within its content based on a search query. This is useful in scenarios where you want to draw attention to specific pieces of text within a larger body of content, such as highlighting search terms in search results or important keywords in a text.

## Use Cases

- Emphasizing search terms in search results.
- Highlighting important keywords in documentation or articles.
- Drawing attention to specific parts of a text in educational materials.

## Anatomy

To use the `Highlight` component, you need to pass the text to be displayed as children and specify the terms to be highlighted through the `query` prop. The component can receive styles to customize the appearance of the highlighted text.

### Basic Implementation

```python
from nextpy.components.chakra.typography import Highlight

highlighted_text = Highlight.create(
    "This is an example of Highlight component in Nextpy.",
    query=["Highlight", "Nextpy"]
)
```

### Advanced Implementation

The advanced implementation may include custom styling and handling of events such as clicks or focus.

```python
from nextpy.components.chakra.typography import Highlight

highlighted_text = Highlight.create(
    "Custom styling and events in the Highlight component.",
    query=["styling", "events"],
    styles={"color": "blue", "fontWeight": "bold"},
    on_click=lambda event: print("Text clicked")
)
```

## Components

The `Highlight` component is a single entity and doesn't have sub-components, but its properties can be used to control its behavior and appearance.

### Properties Table

| Prop Name      | Type                                    | Description                                            |
| -------------- | --------------------------------------- | ------------------------------------------------------ |
| children       | `str` or `list`                         | The text or texts to be displayed inside the component. |
| query          | `Var[List[str]]` or `List[str]`         | The term or terms to be highlighted within the text.    |
| styles         | `Var[Dict]` or `Dict`                   | Custom style for highlighted text.                      |
| style          | `Style`                                 | The overall style of the component.                     |
| key            | `Any`                                   | A unique key for the component.                         |
| id             | `Any`                                   | The id for the component.                               |
| class_name     | `Any`                                   | The class name for the component.                       |
| autofocus      | `bool`                                  | Whether the component should autofocus on page load.    |
| custom_attrs   | `Dict[str, Union[Var, str]]`            | Custom attributes for the component.                    |
| on_blur        | `EventHandler`, `EventSpec`, etc.       | Event handler for when the component loses focus.       |
| on_click       | `EventHandler`, `EventSpec`, etc.       | Event handler for when the component is clicked.        |
| ...            |                                         | Additional event handlers for various mouse and focus events. |

## Notes

- `query` prop is required to enable the highlighting feature.
- If both `styles` and `style` props are provided, they will apply to the highlighted text and the component, respectively.

## Best Practices

- Use a list of strings for the `query` prop for multiple search terms.
- Provide specific styles for the highlighted text to make it stand out.
- Attach event handlers such as `on_click` if interaction with the highlighted text is necessary.

The `Highlight` component in Nextpy is a powerful tool for drawing attention to specific parts of your text content. Proper usage of this component enhances the user experience by making important text immediately visible and interactive when needed.