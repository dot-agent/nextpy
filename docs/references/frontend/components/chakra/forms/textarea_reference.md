##  Reference for nextpy/frontend/components/chakra/forms/textarea.pyi

# TextArea Component Documentation

## Overview

The `TextArea` component in the Nextpy library is designed to allow users to input multi-line text. It's a form control that can be useful in various scenarios where you need to collect longer, free-form text from a user, such as comments, descriptions, or feedback forms.

## Anatomy

The `TextArea` component can be used in its simplest form or customized with various props to meet the needs of your application.

### Basic Usage:

Here's a basic example of how to use the `TextArea` component:

```python
from nextpy.components.chakra.forms.textarea import TextArea
from nextpy.backend.vars import Var

# Creating a state variable to hold the text area value
text_area_value = Var("")

# Creating a TextArea component with binding to the state variable
text_area = TextArea.create(value=text_area_value, placeholder="Enter your text here...")
```

### Advanced Usage:

For more advanced scenarios, you can customize the `TextArea` with additional props:

```python
# Customizing the TextArea with error and focus border colors, and event handlers
text_area_custom = TextArea.create(
    value=text_area_value,
    placeholder="Enter your text here...",
    error_border_color="red.500",
    focus_border_color="blue.500",
    on_change=lambda event: print("Text changed!", event.value),
    on_focus=lambda event: print("Focused!"),
    on_blur=lambda event: print("Blurred!")
)
```

## Components

The `TextArea` component has several properties you can use to customize its behavior and appearance:

| Prop Name           | Type                      | Description                                                  |
|---------------------|---------------------------|--------------------------------------------------------------|
| value               | `Union[Var[str], str]`    | State variable to bind the input value.                      |
| default_value       | `Union[Var[str], str]`    | The default value of the textarea.                           |
| placeholder         | `Union[Var[str], str]`    | The placeholder text displayed when the textarea is empty.   |
| error_border_color  | `Union[Var[str], str]`    | The border color when the textarea is invalid.               |
| focus_border_color  | `Union[Var[str], str]`    | The border color when the textarea is focused.               |
| is_disabled         | `Union[Var[bool], bool]`  | If `True`, the textarea will be disabled.                    |
| is_invalid          | `Union[Var[bool], bool]`  | If `True`, the textarea will display as invalid.             |
| is_read_only        | `Union[Var[bool], bool]`  | If `True`, the textarea will be read-only.                   |
| is_required         | `Union[Var[bool], bool]`  | If `True`, the textarea will be required.                    |
| variant             | `LiteralInputVariant`     | Style variant: "outline", "filled", "flushed", or "unstyled" |
| name                | `Union[Var[str], str]`    | The name of the textarea form field.                         |
| style               | `Style`                   | Style object to customize component styles.                  |
| autofocus           | `bool`                    | If `True`, the textarea will be automatically focused.       |
| custom_attrs        | `Dict[str, Union[Var, str]]` | Custom attributes for the textarea element.             |
| on_blur             | `EventHandler`            | Event handler for the blur event.                            |
| on_change           | `EventHandler`            | Event handler for the change event.                          |
| on_click            | `EventHandler`            | Event handler for the click event.                           |
| ...                 | ...                       | Other event handlers for standard HTML events.               |

## Notes

- Ensure that you bind the `value` prop to a `Var` if you want to manage the textarea's value reactively.
- If you use both `value` and `default_value`, the `value` prop will take precedence.

## Best Practices

- Use the `placeholder` prop to provide a hint to the user about what to enter in the textarea.
- When using `variant`, choose a style that is consistent with the rest of your application for a uniform look.
- Always include the appropriate event handlers (`on_change`, `on_blur`, etc.) to manage the state and validate the user input.
- Utilize the `is_required`, `is_read_only`, and `is_disabled` props to guide user interaction based on the context of the form.

When writing documentation for Nextpy's `TextArea`, be sure to provide clear code examples, explain the purpose and usage of each prop, and offer guidance on best practices to help developers create effective and user-friendly forms in their applications.