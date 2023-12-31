##  Reference for nextpy/frontend/components/next/image(Generated by a LLM. Pending Review)

# Nextpy Image Component Documentation

## Image

The `Image` component in Nextpy is designed for displaying images with built-in optimization and enhancement features. It can handle both external and internal images and provides various options for loading, sizing, and placeholder strategies.

### Anatomy

#### Basic Usage

To display an image using Nextpy, you need to set the `src` attribute to the image URL or path, and optionally set `width` and `height` for sizing:

```python
from nextpy.components.next import Image

image = Image.create(
    src="https://example.com/image.jpg",
    width=500,
    height=300,
    alt="A description of the image"
)
```

#### Advanced Usage

For advanced scenarios, you can customize the image loading strategy, specify a placeholder, and use event handlers:

```python
image = Image.create(
    src="/path/to/internal/image.jpg",
    width=Var(500),  # Dynamic width
    height=Var(300),  # Dynamic height
    alt="A description of the image",
    placeholder="blur",
    blurDataURL="data:image/jpeg;base64,...",  # Base64 encoded image
    on_load=EventHandler(lambda event: print("Image loaded")),
    on_error=EventHandler(lambda event: print("Image failed to load"))
)
```

### Components

#### Properties

| Prop Name      | Type                            | Description |
| -------------- | ------------------------------- | ----------- |
| `width`        | `Optional[Union[str, int]]`     | The width of the image, can be a fixed value or a percentage. |
| `height`       | `Optional[Union[str, int]]`     | The height of the image, similar to width. |
| `src`          | `Optional[Union[Var[Any], Any]]`| The source URL or path of the image. |
| `alt`          | `Optional[Union[Var[str], str]]`| Alternative text for the image, crucial for accessibility. |
| `loader`       | `Optional[Union[Var[Any], Any]]`| A custom function for resolving image URLs. |
| `fill`         | `Optional[Union[Var[bool], bool]]`| If `True`, the image will scale to fill its container. |
| `sizes`        | `Optional[Union[Var[str], str]]`| A string that specifies image sizes for different viewport breakpoints. |
| `quality`      | `Optional[Union[Var[int], int]]`| Image quality setting, ranging from 1 to 100. |
| `priority`     | `Optional[Union[Var[bool], bool]]`| If `True`, the image will preload and have higher loading priority. |
| `placeholder`  | `Optional[Union[Var[str], str]]`| Specifies a placeholder to show before image loads. Can be `blur`, `empty`, or a data URL. |
| `loading`      | `Optional[Union[Var[Literal["lazy", "eager"]], Literal["lazy", "eager"]]]`| The loading strategy, either lazy or eager. |
| `blurDataURL`  | `Optional[Union[Var[str], str]]`| Base64 encoded string for a placeholder blur image. |
| `style`        | `Optional[Style]`               | The inline styles to apply to the image element. |
| `key`          | `Optional[Any]`                 | A unique key for the component instance. |
| `id`           | `Optional[Any]`                 | The DOM id attribute value. |
| `class_name`   | `Optional[Any]`                 | The CSS class name(s) for the image. |
| `autofocus`    | `Optional[bool]`                | Auto-focus the image when the component mounts. |
| `custom_attrs` | `Optional[Dict[str, Union[Var, str]]]`| Custom HTML attributes for the image. |

#### Event Triggers

| Event Name      | Description |
| --------------- | ----------- |
| `on_blur`       | Triggered when the image loses focus. |
| `on_click`      | Triggered when the image is clicked. |
| `on_context_menu`| Triggered when the context menu is invoked on the image. |
| `on_double_click`| Triggered on a double click on the image. |
| `on_error`      | Triggered if the image fails to load. |
| `on_focus`      | Triggered when the image gains focus. |
| `on_load`       | Triggered when the image has finished loading. |
| `on_mount`      | Triggered when the image is mounted to the DOM. |
| `on_mouse_down` | Triggered when a mouse button is pressed on the image. |
| `on_mouse_enter`| Triggered when the mouse pointer enters the image area. |
| `on_mouse_leave`| Triggered when the mouse pointer leaves the image area. |
| `on_mouse_move` | Triggered when the mouse pointer moves over the image. |
| `on_mouse_out`  | Triggered when the mouse pointer moves out of the image. |
| `on_mouse_over` | Triggered when the mouse pointer is over the image. |
| `on_mouse_up`   | Triggered when a mouse button is released over the image. |
| `on_scroll`     | Triggered when the image is scrolled. |
| `on_unmount`    | Triggered when the image is unmounted from the DOM. |

### Notes

- The `src` attribute is mandatory and must point to a valid image URL or path.
- If `width` and `height` are not specified, the image size will default to the size of the image file.
- `fill` defaults to `True`, allowing the image to adapt to its container's dimensions.
- It's important to provide the `alt` text for accessibility reasons, especially for screen readers.

### Best Practices

- Use `width` and `height` to prevent layout shift as the image loads.
- Provide `alt` text for all images to support users who rely on screen readers.
- Consider the `loading` attribute to improve performance, using "lazy" for offscreen images and "eager" for critical images.
- Use `priority` for above-the-fold images to ensure they load quickly.
- Optimize the size and format of images before using them to reduce load times and improve performance.

This documentation should serve as a foundational guide for developers to effectively leverage the `Image` component in their Nextpy applications, ensuring that images are efficiently and responsively integrated into their web applications.