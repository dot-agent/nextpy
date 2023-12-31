##  Reference for nextpy/frontend/components/next/video(Generated by a LLM. Pending Review)

# Nextpy `Video` Component Documentation

## Video

The `Video` component allows you to embed a video player in your Nextpy application. It is useful for playing video content from a given source (URL) and offers typical video player functionalities like play, pause, and seeking. This component is essential for applications that require video playback capabilities.

### Anatomy

To use the `Video` component, you need to import it from `nextpy.components.next` and create an instance of it by calling the `Video.create()` method. Here's a basic example:

```python
from nextpy.components.next import Video

video_player = Video.create(
    src="http://example.com/path/to/video.mp4"
)
```

#### Advanced Usage

For more advanced cases, you can specify additional options:

```python
video_player = Video.create(
    src="http://example.com/path/to/video.mp4",
    style=your_style_object,
    autoplay=True,
    loop=True,
    muted=True,
    controls=True
)
```

### Components

The `Video` component has several properties that you can use to customize its behavior:

| Prop Name     | Type                                             | Description                                    |
|---------------|--------------------------------------------------|------------------------------------------------|
| `src`         | `Optional[Union[Var[str], str]]`                 | The URL of the video to play.                  |
| `style`       | `Optional[Style]`                                | Style object to apply custom CSS to the video. |
| `autoplay`    | `Optional[bool]`                                 | Automatically start playing the video.         |
| `loop`        | `Optional[bool]`                                 | Loop the video when it reaches the end.        |
| `muted`       | `Optional[bool]`                                 | Start the video in muted mode.                 |
| `controls`    | `Optional[bool]`                                 | Show playback controls.                        |
| `key`         | `Optional[Any]`                                  | A unique key for the component.                |
| `id`          | `Optional[Any]`                                  | The DOM id for the component.                  |
| `class_name`  | `Optional[Any]`                                  | The class name for the component.              |
| `autofocus`   | `Optional[bool]`                                 | Autofocus the component on page load.          |
| `custom_attrs`| `Optional[Dict[str, Union[Var, str]]]`           | Custom HTML attributes for the video element.  |

The `Video` component also supports various event handlers like `on_click`, `on_mouse_enter`, `on_mouse_leave`, and more, allowing developers to add interactivity to the video player.

### Notes

- Ensure that the video source URL (`src`) is accessible and points to a valid video file.
- For the autoplay feature to work, the browser may require the video to be muted due to autoplay policies.

### Best Practices

- When using autoplay, consider adding the `muted` attribute to comply with browser policies and enhance user experience.
- Use the `controls` attribute to provide users with the ability to interact with video playback.
- Always provide a `key` if the `Video` component is used within a list of items or is dynamically generated.

Remember to keep the user experience in mind while embedding videos in your application, taking into account factors like loading times and data usage, especially for users on mobile devices with limited data plans.