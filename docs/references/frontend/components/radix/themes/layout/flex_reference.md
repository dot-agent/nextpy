##  Reference for nextpy/frontend/components/radix/themes/layout/flex(Generated by a LLM. Pending Review)

# Nextpy `Flex` Component Documentation

## Flex

The `Flex` component is a layout utility that extends the functionality of a standard `div` element to provide flexible, responsive layout capabilities using CSS Flexbox. It is designed to allow developers to easily manage the layout of their web application's UI by controlling the positioning and alignment of child elements within a flex container.

### Anatomy

To use the `Flex` component, import it from the Nextpy library and instantiate it with the desired properties. You can add child components directly within the `Flex` container.

#### Basic Usage

```python
from nextpy.components.radix.themes.layout.flex import Flex

flex_container = Flex.create(
    # Child components go here
)
```

#### Advanced Usage

```python
flex_container = Flex.create(
    # Child components go here
    direction="row",
    align="center",
    justify="space-between",
    wrap="wrap",
    gap="2",
    style=Style(background_color="lightgrey", padding="10px")
)
```

### Components

The `Flex` component has a variety of properties that you can use to customize its behavior and appearance. Below is a detailed description of each sub-component property.

#### Properties Table

| Prop Name        | Type    | Description |
| ---------------- | ------- | ----------- |
| `color`          | Var[str], str | Sets the text color of the container. |
| `color_scheme`   | Var[Literal], Literal | Defines a color scheme for the container from a predefined set of colors. |
| `as_child`       | Var[bool], bool | Renders the component as a child of another, merging props and behavior. |
| `display`        | Var[Literal], Literal | Controls the display property: "none", "inline-flex", or "flex". |
| `direction`      | Var[Literal], Literal | Specifies the flex direction: "row", "column", "row-reverse", or "column-reverse". |
| `align`          | Var[Literal], Literal | Aligns children along the main axis: "start", "center", "end", "baseline", "stretch". |
| `justify`        | Var[Literal], Literal | Justifies children along the cross axis: "start", "center", "end", "between". |
| `wrap`           | Var[Literal], Literal | Controls whether children should wrap: "nowrap", "wrap", "wrap-reverse". |
| `gap`            | Var[Literal], Literal | Sets the gap between children: "1" to "9". |
| ...              | Var, str | Other HTML attributes such as `access_key`, `auto_capitalize`, etc. |
| `style`          | Style | The inline style for the component. |
| `key`            | Any | A unique key for the component. |
| `id`             | Any | The id for the component. |
| `class_name`     | Any | The class name for the component. |
| `autofocus`      | bool | If true, the component will be focused on page load. |
| `custom_attrs`   | Dict[str, Union[Var, str]] | Custom attributes for the component. |

#### Event Triggers

The `Flex` component supports various event triggers such as `on_blur`, `on_click`, `on_context_menu`, etc. These allow you to specify behavior when certain user interactions occur.

### Notes

- Remember that the `Flex` component is an extension of a `div` element, so it can accept all the standard HTML attributes and events.
- Using `Flex` with no properties will default to a block-level container with no special flex behaviors.

### Best Practices

- Use the `Flex` component to build responsive designs that adapt to different screen sizes.
- When using `gap`, ensure that you have a corresponding CSS rule to support the spacing, or use the predefined `gap` values.
- Utilize `align` and `justify` to control the alignment of child components within the `Flex` container effectively.
- Prefer using `Flex` over manual `div` styling when you need a quick and easy way to create layouts with consistent spacing and alignment.

By following the guidelines above, you can create clear and effective documentation for the `Flex` component of the Nextpy library. Ensure that all code snippets are tested and functional, and that the documentation is updated regularly to reflect any changes to the API.