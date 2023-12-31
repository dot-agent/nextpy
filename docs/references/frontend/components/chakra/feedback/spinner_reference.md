##  Reference for nextpy/frontend/components/chakra/feedback/spinner(Generated by a LLM. Pending Review)

# Spinner Component Documentation

## Overview

The `Spinner` component in Nextpy is a visual indicator that communicates to users that an action is in progress. It is commonly used when retrieving data or during the loading of a component or page. The `Spinner` is part of Nextpy's Chakra UI component library, which provides a set of accessible, reusable, and composable React components that make it easy to create beautiful, responsive, and interactive user interfaces.

## Anatomy

The `Spinner` component is straightforward to implement. Here are code snippets showcasing basic and advanced usage:

### Basic Implementation

```python
from nextpy.components.chakra.feedback import Spinner

# Basic spinner with default settings
spinner = Spinner.create()
```

### Advanced Implementation

```python
from nextpy.components.chakra.feedback import Spinner

# Advanced spinner with customized properties
spinner = Spinner.create(
    empty_color="gray.200",
    label="Loading...",
    speed="0.8s",
    thickness=4,
    size="lg",
    style=Style(bg_color="white", padding="10px"),
)
```

## Components

The `Spinner` component is a standalone component with the following properties:

| Prop Name     | Type                                                        | Description                                                                                    |
|---------------|-------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| empty_color   | `Union[Var[str], str]`                                      | The color of the empty area in the spinner.                                                    |
| label         | `Union[Var[str], str]`                                      | Accessibility label with a fallback loading text for screen readers.                            |
| speed         | `Union[Var[str], str]`                                      | The speed of the spinner animation. Must be a string representing seconds (e.g., `'0.45s'`).    |
| thickness     | `Union[Var[int], int]`                                      | The thickness of the spinner.                                                                  |
| size          | `Union[Var[Literal["sm", "md", "lg", "xs", "xl"]], Literal]`| The size of the spinner (`'xs'`, `'sm'`, `'md'`, `'lg'`, `'xl'`).                              |
| style         | `Optional[Style]`                                           | The style properties for the component.                                                        |
| key           | `Any`                                                       | A unique key for the component.                                                                |
| id            | `Any`                                                       | The HTML id attribute for the component.                                                       |
| class_name    | `Any`                                                       | The HTML class attribute for the component.                                                    |
| autofocus     | `bool`                                                      | If true, the component will be focused automatically when the page loads.                      |
| custom_attrs  | `Dict[str, Union[Var, str]]`                                | Custom attributes for the spinner.                                                             |
| on_*          | Various EventHandlers                                       | Event handlers for various user actions like click, mouse enter, focus, blur, etc.             |
| **props       | Various                                                     | Additional properties that can be passed to the component.                                     |

## Notes

- Ensure the spinner is used in situations where the wait time is perceptible to the user to avoid unnecessary distractions.
- Always provide a label for accessibility reasons to indicate what is loading.

## Best Practices

- Use the `Spinner` for giving feedback on an ongoing process which may take time.
- Avoid overusing spinners, as they can make an application feel slower if used excessively.
- Customize the spinner's appearance (color, size, thickness) to match the application's design and improve user experience.
- Remember to manage the spinner's visibility, showing it when the process starts and hiding it once the process is complete.