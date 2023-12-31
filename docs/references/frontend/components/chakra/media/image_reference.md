##  Reference for nextpy/frontend/components/chakra/media/image(Generated by a LLM. Pending Review)

# Nextpy Documentation: Image Component

## Image Component Overview

The `Image` component in the Nextpy library is used for displaying images in a Nextpy application. It provides a convenient wrapper around the standard HTML `<img>` element, with additional features for handling image loading states and fallbacks.

### Use Cases

- Displaying static images from local assets or URLs.
- Incorporating responsive images using the `srcSet` attribute.
- Showing placeholders or alternative content while the image is loading or if it fails to load.
- Implementing custom image loading strategies, such as lazy loading.

### Structure and Usage

The `Image` component can be used directly in your Nextpy application by importing it from the `nextpy/components/chakra/media/image.py` module.

```python
from nextpy.components.chakra.media.image import Image
```

Here is a simple example of how to use the `Image` component:

```python
image = Image.create(src="path/to/your/image.jpg", alt="Description of the image")
```

## Anatomy

### Basic Implementation

Here is a basic code snippet that shows the usage of the `Image` component:

```python
from nextpy.components.chakra.media.image import Image

# Basic image usage
image = Image.create(
    src="path/to/your/image.jpg",
    alt="Description of the image"
)
```

### Advanced Implementation

A more advanced example of the `Image` component might include handling events and specifying fallback content:

```python
from nextpy.components.chakra.media.image import Image
from nextpy.frontend.components.basic import Text

# Advanced image usage with fallback and events
image_with_fallback = Image.create(
    src="path/to/your/image.jpg",
    alt="Description of the image",
    fallback=Text.create("Image failed to load"),
    on_error=lambda event: print("Image failed to load"),
    on_load=lambda event: print("Image has loaded"),
    loading="lazy"
)
```

## Components

### Properties Table

| Prop Name      | Type                                              | Description                                                  |
|----------------|---------------------------------------------------|--------------------------------------------------------------|
| `src`          | `Union[Var[Any], Any]`                            | The path/url to the image or PIL image object.               |
| `alt`          | `Optional[Union[Var[str], str]]`                  | The alt text of the image.                                   |
| `fallback`     | `Optional[Component]`                             | Fallback Nextpy component to show if image loading fails.    |
| `fallback_src` | `Optional[Union[Var[str], str]]`                  | Fallback image source if image loading fails.                |
| `loading`      | `Optional[Union[Var[Literal["eager", "lazy"]], Literal["eager", "lazy"]]]` | Loading strategy ("eager" or "lazy"). |
| `style`        | `Optional[Style]`                                 | The style of the component.                                  |
| `...`          |                                                   | Additional standard HTML attributes and custom event handlers.|

### Event Triggers

- `on_error`: Triggered if there is an error loading the image.
- `on_load`: Triggered when the image has successfully loaded.
- `on_click`: Triggered when the image is clicked.
- More event handlers for common mouse and focus events.

## Notes

- The `src` attribute is mandatory and should point to a valid image source.
- The `alt` attribute is highly recommended for accessibility purposes.
- The `loading` attribute can be set to `"lazy"` for lazy loading, which can improve performance for offscreen images.

## Best Practices

- Always provide the `alt` attribute to describe the image content for screen readers and in cases where the image cannot be displayed.
- Use the `loading="lazy"` attribute for images that are not immediately visible to reduce initial page load time.
- Optimize images for the web to ensure fast loading times and reduced bandwidth usage.
- Consider specifying `fallback` content or `fallback_src` to improve user experience when images fail to load.
- For responsive images, use the `src_set` property to provide different image resolutions.
- Remember to handle the `on_error` event to provide feedback or alternatives when images cannot be loaded.