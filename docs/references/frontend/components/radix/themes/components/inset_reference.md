##  Reference for nextpy/frontend/components/radix/themes/components/inset(Generated by a LLM. Pending Review)

# Nextpy - Inset Component

## Overview

The `Inset` component in the Nextpy library is a versatile container that provides padding control and color scheme options to its child elements. It extends the `Div` component and includes common margin properties, as well as theming capabilities from `RadixThemesComponent`. This component is useful when you want to create a section within your UI that has consistent spacing around its content.

## Anatomy

### Basic Implementation

```python
from nextpy.components.radix.themes.components.inset import Inset

# Basic Inset with default padding and color scheme
inset_example = Inset.create(
    "This is a basic inset",
    p="4"  # Padding value can be a string or integer
)
```

### Advanced Implementation

```python
from nextpy.components.radix.themes.components.inset import Inset

# Advanced Inset with specific padding values and color scheme
advanced_inset = Inset.create(
    "This is an advanced inset with specific padding and color scheme",
    px="4",  # Horizontal padding
    py="2",  # Vertical padding
    color_scheme="blue",  # Color scheme from the predefined list
    style=Style(background_color="#f0f0f0")  # Custom style
)
```

## Components

The `Inset` component has several properties that can be configured:

| Prop Name        | Type                                                    | Description                                             |
|------------------|---------------------------------------------------------|---------------------------------------------------------|
| `color`          | `str`, `Var[str]`                                       | Maps to the CSS default color property.                  |
| `color_scheme`   | `Literal[tomato, red, ..., gray]`, `Var[Literal[...]]`  | Maps to the radix color property.                        |
| `side`           | `Literal[x, y, top, bottom, right, left]`, `Var[...]`   | Specifies the side where the padding should be applied.  |
| `clip`           | `Literal[border-box, padding-box]`, `Var[...]`          | Defines the box model used for calculating paddings.     |
| `p`, `px`, `py`  | `int`, `str`, `Var[...]`                                | Padding value for the specified side(s).                 |
| `pt`, `pr`, `pb` | `int`, `str`, `Var[...]`                                | Padding value for top, right, and bottom respectively.   |
| `pl`             | `int`, `str`, `Var[...]`                                | Padding value for left.                                  |
| ...              | ...                                                     | Additional HTML attributes and event handlers.           |

*Note: All padding props (`p`, `px`, `py`, `pt`, `pr`, `pb`, `pl`) support both numeric values and string literals for predefined spacing scales.*

## Notes

- When using the `Inset` component, ensure that any child components are compatible with the padding and margin props being used.
- The `color_scheme` should be chosen from the predefined set of colors supported by the Radix theme.
- Custom styles can be applied using the `style` prop, allowing for further customization of the `Inset`.

## Best Practices

- Use the `Inset` component to manage consistent spacing within sections of your application.
- Prefer using predefined color schemes for a consistent and theme-compliant UI.
- Utilize specific padding props (`pt`, `pr`, `pb`, `pl`) when you need different padding values on different sides of the container.
- When customizing styles, ensure they don't conflict with the `color_scheme` and padding props to maintain the visual integrity of the UI.

Remember to test different combinations of properties to achieve the desired layout and aesthetics for your application. The `Inset` component is a simple yet powerful tool for creating neatly organized UI sections with proper spacing and theming.