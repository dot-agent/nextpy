##  Reference for nextpy/frontend/components/el/elements/media(Generated by a LLM. Pending Review)

# Nextpy Documentation: Media Components

## Overview

Media components in Nextpy are designed to embed multimedia content such as images, audio, video, and other embedded content like SVGs and objects. These components are essential for developers who want to create interactive and engaging web applications.

## Anatomy

Below are examples and descriptions of how to use different media components in Nextpy.

### Area

The `Area` component defines a clickable area within an image map.

```python
Area.create(
    href="https://example.com",
    alt="Example Area",
    shape="rect",
    coords="34,44,270,350",
    target="_blank"
)
```

### Audio

The `Audio` component is used to embed sound content in documents. It can display a set of audio controls for playing sound.

```python
Audio.create(
    src="path/to/audio.mp3",
    controls=True,
    auto_play=False,
    loop=True
)
```

### Img

The `Img` component represents an image in the document.

```python
Img.create(
    src="path/to/image.jpg",
    alt="Description of the image",
    width="500",
    height="300"
)
```

### Map

The `Map` component defines an image map used by `Area` components.

```python
Map.create(
    name="mapname",
    children=[
        Area.create(shape="rect", coords="34,44,270,350", href="https://example.com")
    ]
)
```

### Track

The `Track` component is used as a child of the `Audio` or `Video` components to specify text tracks for media elements.

```python
Video.create(
    children=[
        Track.create(kind="subtitles", src="subtitles_en.vtt", srclang="en", label="English")
    ]
)
```

### Video

The `Video` component is used to embed video content.

```python
Video.create(
    src="path/to/video.mp4",
    controls=True,
    width="640",
    height="360"
)
```

### Embed

The `Embed` component provides a container for external (non-HTML) content.

```python
Embed.create(src="path/to/plugin", type="application/pdf", width="500", height="500")
```

### Iframe

The `Iframe` component represents a nested browsing context, embedding another HTML page into the current one.

```python
Iframe.create(src="https://example.com", width="600", height="400")
```

### Object

The `Object` component represents an external resource, which can be treated as an image, a nested browsing context, or a resource to be handled by a plugin.

```python
Object.create(data="path/to/object", type="application/pdf", width="400", height="300")
```

### Picture

The `Picture` component is used as a container for multiple `Img` elements to provide alternative versions of an image for different display/device scenarios.

```python
Picture.create(
    children=[
        Source.create(src_set="image-320w.jpg", media="(max-width: 320px)"),
        Img.create(src="image.jpg", alt="Description of the image")
    ]
)
```

### Portal

The `Portal` component is used to render children into a DOM node that exists outside the DOM hierarchy of the parent component.

```python
Portal.create(
    children=[
        # Your portal content goes here
    ]
)
```

### Source

The `Source` component is used to specify multiple media resources for `Picture`, `Audio`, and `Video` components.

```python
Video.create(
    children=[
        Source.create(src="movie.mp4", type="video/mp4"),
        Source.create(src="movie.ogg", type="video/ogg")
    ]
)
```

### Svg

The `Svg` component is a container for SVG graphics.

```python
Svg.create(
    width="100",
    height="100",
    children=[
        Path.create(d="M10 10 H 90 V 90 H 10 L 10 10")
    ]
)
```

## Notes

- Ensure that media elements are accessible by providing `alt` text for images and transcripts for audio and video.
- For `Video` and `Audio` components, consider providing a fallback content for browsers that do not support these elements.

## Best Practices

- Use responsive images with `SrcSet` and `Sizes` attributes to optimize loading times and bandwidth usage.
- Employ lazy loading of offscreen images and iframes to improve performance (`loading="lazy"`).
- When using the `Embed`, `Object`, or `Iframe` components, be cautious about security and privacy implications and apply the appropriate attributes (e.g., `sandbox` for `Iframe`).

Remember to test different media types and formats for compatibility across various browsers and devices.