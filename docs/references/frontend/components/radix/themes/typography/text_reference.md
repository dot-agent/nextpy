##  Reference for nextpy/frontend/components/radix/themes/typography/text(Generated by a LLM. Pending Review)

# Nextpy `Text` Component Documentation

## Text

The `Text` component is a fundamental building block for creating text elements within a Nextpy application. It extends the `el.Span` element, incorporating common margin properties and radix theme support to allow for a wide range of styling options.

### Purpose

The `Text` component is used to display inline text content with various customization options such as color, size, weight, and alignment. It is suitable for anything from small labels to large headings and body text.

### Use Cases

- Displaying headings, paragraphs, labels, or any inline text element.
- Customizing text appearance according to the design system or theme.
- Implementing text with responsive margins and alignment.

### Anatomy

The `Text` component can be created with a range of properties that control its appearance and behavior. Here's an example of how to use it:

```python
from nextpy.components.radix.themes.typography.text import Text

# Basic usage
simple_text = Text.create("Hello, Nextpy!")

# Advanced usage with various properties
styled_text = Text.create(
    "Stylish Text",
    color="blue",
    size="5",
    weight="bold",
    align="center",
    trim="both",
    high_contrast=True,
    m="4",
    style=Style(padding="10px", background_color="#f0f0f0"),
)
```

### Components

The `Text` component accepts a number of sub-components and properties:

#### Properties Table

| Prop Name        | Type                                     | Description |
| ---------------- | ---------------------------------------- | ----------- |
| color            | `Var[str]`, `str`                        | Maps to CSS default color property. |
| color_scheme     | `Var[LiteralAccentColor]`, `LiteralAccentColor` | Maps to radix color property. |
| size             | `Var[LiteralTextSize]`, `LiteralTextSize` | Size of the text ranging from "1" to "9". |
| weight           | `Var[LiteralTextWeight]`, `LiteralTextWeight` | Thickness of the text: "light", "regular", "medium", "bold". |
| align            | `Var[LiteralTextAlign]`, `LiteralTextAlign` | Alignment of text within the element: "left", "center", "right". |
| trim             | `Var[LiteralTextTrim]`, `LiteralTextTrim` | Controls trimming of whitespace. |
| high_contrast    | `Var[bool]`, `bool`                      | Renders the text with higher contrast color. |
| m                | `Var[LiteralMargin]`, `LiteralMargin`    | Margin size ranging from "1" to "9". |
| mx               | `Var[LiteralMargin]`, `LiteralMargin`    | Horizontal margin size ranging from "1" to "9". |
| my               | `Var[LiteralMargin]`, `LiteralMargin`    | Vertical margin size ranging from "1" to "9". |
| mt               | `Var[LiteralMargin]`, `LiteralMargin`    | Margin-top size ranging from "1" to "9". |
| ... (other props)| Various                                  | Additional HTML attributes and event handlers. |

#### Event Triggers

- `on_click`: Triggered when the text is clicked.
- `on_mouse_enter`: Triggered when the mouse enters the text area.
- `on_focus`: Triggered when the text gains focus.
- ... (more standard HTML event handlers)

### Notes

- The `as_child` property is used to replace the default rendered element with a child component, merging their properties and behavior.
- When using `color_scheme`, ensure that it aligns with the application's design system or the radix theme color palette.

### Best Practices

- Use semantic property names like `size`, `weight`, and `align` to keep the component's API intuitive.
- Avoid inline styles when possible and prefer using the `style` property for complex styling needs.
- Leverage the radix theme properties to maintain consistency across the application's UI.
- Use appropriate event handlers for interactivity but avoid excessive JavaScript execution on events like `on_mouse_move`.

Remember to maintain a balance between flexibility and simplicity to ensure that developers can easily use the `Text` component in various scenarios without being overwhelmed by too many options.