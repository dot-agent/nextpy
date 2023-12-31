##  Reference for nextpy/frontend/page

# `page` Decorator

## Overview

The `page` decorator in the Nextpy library is an essential tool for defining web pages within a full-stack Python application. This decorator allows developers to associate Python functions with specific URLs, making it possible to create dynamic content that responds to user interactions. It can be used to set up the page's route, title, meta tags, and other attributes that are crucial for SEO and user experience.

## Use Cases

- Creating individual web pages with unique routes within a Nextpy application.
- Setting SEO-friendly page titles, descriptions, and image previews for sharing on social media.
- Injecting custom script tags for enhanced functionality or analytics.
- Registering event handlers that trigger when the page is loaded.

## Anatomy

### Basic Implementation

```python
import nextpy as xt

@xt.page(route='/welcome', title='Welcome Page')
def welcome_page():
    # Page content and components go here
    pass
```

### Advanced Implementation

```python

def on_page_load():
    print("Page has been loaded!")

@xt.page(
    route='/profile',
    title='User Profile',
    image='path/to/image.png',
    description='View and edit your user profile',
    meta='profile, user',
    script_tags=[],
    on_load=EventHandler(on_page_load)
)
def profile_page():
    # Page content and components go here
    pass
```

## Components

### `xt.page` Decorator Properties Table

| Prop Name    | Type                                   | Description                                                     |
|--------------|----------------------------------------|-----------------------------------------------------------------|
| `route`      | `str` \| `None`                        | The URL path that the page will respond to.                     |
| `title`      | `str` \| `None`                        | The title of the page, which is displayed in the browser tab.   |
| `image`      | `str` \| `None`                        | The URL or path to an image for social media sharing previews.  |
| `description`| `str` \| `None`                        | A brief description of the page's content for SEO purposes.     |
| `meta`       | `str` \| `None`                        | Additional meta tags for the head section of the page.          |
| `script_tags`| `list[Component]` \| `None`            | Custom script tags to be included in the page.                  |
| `on_load`    | `EventHandler` \| `list[EventHandler]` \| `None` | Event handlers triggered when the page is loaded.              |

### Event Triggers

- `on_load`: This event is triggered when the page is fully loaded. It allows developers to execute certain actions, such as initializing components or fetching data.

## Notes

- The `route` parameter must be unique across all decorated pages to avoid routing conflicts.
- Static assets like images should be properly managed and served to ensure they are accessible when referenced in the `image` parameter.
- Event handlers should be used with care to avoid performance issues, especially when dealing with large amounts of data or complex initializations.

## Best Practices

- Always provide a meaningful `title` and `description` to improve the page's findability and relevance in search engine results.
- When using `script_tags`, make sure to include scripts that are necessary for the page to prevent unnecessary loading times and potential conflicts.
- Utilize `on_load` handlers to improve user experience by showing loaders or placeholders until the page is fully ready for interaction.

## Additional Functions

### `get_decorated_pages`

This utility function returns a list of dictionaries containing the decorated pages' metadata. It is typically used internally within the Nextpy framework to manage and serve the defined pages.

```python
from nextpy import get_decorated_pages

pages_metadata = get_decorated_pages()
# This will contain information about all pages decorated with @xt.page
```