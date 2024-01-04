# Pages

- Pages are the building blocks of Nextpy apps, defining components that display content at specific URLs.
- Routing is the mechanism that maps URLs to page functions, directing users to the appropriate content.


### Creating a Page

A page is created by defining a function that returns a component. This function can be associated with a specific URL route.

- **Default Route**: By default, the function name is used as the route.
- **Custom Route**: You can specify a custom route using the `route` parameter.
**Example:**

```python

# the `index` function defines the root page of the application, which is accessible at the `http://localhost:3000/` URL.
@xt.page()
def index():
    return xt.text("Welcome to the Index Page")

# the `gallery` function defines a page accessible at the `http://localhost:3000/gallery/` URL. here the function name is used as the route.
@xt.page()
def gallery():
    return xt.text("Explore the Gallery of Wonders")

# The `secret` function is accessible at the `http://localhost:3000/secret-garden` URL.
@xt.page(route="/secret-garden")
def secret_garden():
    return xt.text("Shh... You've Discovered the Secret Garden")

app = xt.App()

```

### `@xt.page` decorator 

The `@xt.page` decorator simplifies the process of associating routes with components. This is functionally equivalent to calling `app.add_page` with the same arguments.

**Here's how it works:**

1. **Create a function that returns a Nextpy component.**
2. **Add the `@xt.page` decorator above the function.**
3. **Optionally, customize the route and title parameters:**
   - `route`: Specify the URL path for the page (e.g., `@xt.page(route="/about")`)
   - `title`: Set a descriptive title for the page (e.g., `@xt.page(title="About Page")`)

**Example:**

```python
@xt.page(route="/contact", title="Get in Touch")
def contact_page():
    return xt.heading("Contact Page")  # Your contact form component
```

#### Special Behavior of the Index Route

- **Dual Accessibility**: The `index` route is unique in that it's accessible via both `/` and `/index`. This offers flexibility in how users can reach the main page of your application.
- **Other Pages**: All other pages adhere strictly to their specified routes.

### Nested Routes

Nextpy also supports nested routes, allowing for a hierarchical structure in your application's URLs.

**Example:**

```python

@xt.page(route="/adventure/island")
def island_adventure():
    return xt.text("Embark on the Island Adventure")

```

### Dynamic URLs

Dynamic URLs are a fundamental feature that enables web applications to handle diverse URL structures and generate content dynamically based on user-specified parameters within the URL. Nextpy provides a comprehensive and flexible system for defining and managing dynamic routes.

#### 1. Regular Dynamic Routes

Regular dynamic routes are essential for capturing specific URL segments as parameters. They are defined using square brackets `[]`.

- **Usage and Flexibility**: These routes are incredibly useful for creating pages that depend on variable data, like user IDs, product IDs, or other unique identifiers.

**Example**

```python

class State(xt.State):
    @xt.var
    def chapter(self) -> str:
        return self.router.page.params.get('chapter', 'Intro')

@xt.page(route='/story/[chapter]')
def story_chapter():
    return xt.heading(State.chapter)

```

- Here, each URL like **`/story/chapter1`** unveils a different chapter of the story.

#### 2. Catch-All Routes

Catch-all routes are a step further in dynamic routing, allowing you to capture an indefinite number of URL segments.

- **Syntax and Usage**: Defined using `[...variable]`, these routes can match a series of segments, making them ideal for scenarios where the number of segments in a URL is not fixed.
- **Practical Example**: In a file browser application, where the path can have many segments, catch-all routes can be used to capture the entire path.

**Example**

```python

import nextpy as xt

class State(xt.State):
    @xt.var
    def mystery_clues(self) -> str:
        args = self.router.page.params
        clues = args.get('clues', [])
        return f'You have discovered clues: {", ".join(clues)}'

@xt.page(route='/mystery/[...clues]')
def mystery_path():
    return xt.center(
        xt.text(State.mystery_clues)
    )

# Compile the app with the defined page
app = xt.App(state=State)
app.add_page(mystery_path)
```
#### 3. Optional Catch-All Routes

Optional catch-all routes add an extra layer of flexibility, capturing segments that may or may not be present in the URL.

- **Syntax**: Defined using `[[...variable]]`, they function similarly to regular catch-all routes but are optional.
- **Scenario**: Useful in situations where you want a single route to handle multiple URL structures.

  ```python
    @xt.page(route='/mystery/[[...clues]]')
    def mystery_path():
        return xt.center(
            xt.text(State.mystery_clues)
        )
  ```
#### Optional Catch-All Route & Catch-All Route

**Key Differences:**

| Feature          | Optional Catch-All Route | Catch-All Route       |
|---------------------|--------------------------|------------------------|
| Matches root path | Yes                       | No                     |
| Matches empty path | Yes                       | No                     |
| Syntax            | `[[...variable]]`          | `[...variable]`       |
| Placement          | End of URL pattern        | End of URL pattern     |

**Choosing the Right Route:**

- **Use Optional Catch-All Route** if you want a single route to handle both the root path and nested paths within `/mystery`.
- **Use Catch-All Route** if you only want to match URLs with additional segments after `/mystery`.

**Here's a table illustrating which URLs would match each route type:**

| URL Pattern            | Optional Catch-All Route (`/mystery/[[...clues]]`) | Catch-All Route (`/mystery/[...clues]) |
|------------------------|--------------------------------------------------------|----------------------------------------|
| `/mystery`              | **Matches**                                           | **Does not match**                     |
| `/mystery/clue1`        | **Matches**                                           | **Matches**                            |
| `/mystery/clue1/clue2`   | **Matches**                                           | **Matches**                            |
| `/mystery/category/secret` | **Matches**                                           | **Matches**                            |
| `/mystery/` (empty path) | **Matches**                                           | **Does not match**                     |

#### 4. Nested Dynamic Routes
 You can nest dynamic routes within each other to represent a relationship between different segments.
**Example Route Pattern:**

```
@xt.page(route='/mystery/[mysteryId]/secret/[secretId]/clue/[clueId]')
```

### Retrieving Current Page URL

Nextpy provides functionality to retrieve the current page's path and URL, which is especially useful in scenarios where dynamic content rendering, navigation handling, and route-based logic are required.

- **Route Path (`router.page.path`)**:
    - **Functionality**: Retrieves the pattern of the current route as defined in the router configuration. It's particularly useful for dynamic routes.
    - **Use Case**: In a route like `/products/[id]`, instead of returning the specific ID used in the URL, this attribute returns the pattern `/products/[id]`. It's ideal for understanding the route structure or performing operations based on route patterns.
    - **Example Context**: If your page has a route pattern like `/blog/[article]` and the user is on the page `/blog/latest-updates`, `router.page.path` would return `/blog/[article]`.

- **Actual URL (`router.page.raw_path`)**:
    - **Functionality**: Provides the actual path of the current page as it appears in the browser's address bar. This includes all dynamic segments and query parameters.
    - **Use Case**: Useful for logging, analytics, or when you need to know the exact URL the user is visiting, including any specific identifiers or query parameters.
    - **Example Context**: For a dynamic blog post accessed via `/blog?post_id=123`, this attribute would return the full query string, `/blog?post_id=123`.

#### Example

```python
class State(xt.State):
    @xt.var
    def analyze_current_route(self):
        current_page_route = self.router.page.path
        current_page_url = self.router.page.full_raw_path
        return f"Current page: {current_page_route} ,({current_page_url})"
# Define the page with on_load event
@xt.page()
def index():
    return xt.text(State.analyze_current_route)
app = xt.App()
app.add_page(index)
```

In this example, `route_pattern` and `full_path` are used to demonstrate the differences between the route pattern and the actual URL path. The `print` statements provide a clear way to understand what each attribute returns.

#### Obtaining the Complete URL

The complete URL of the current page, including the domain and protocol, is essential in scenarios where absolute references are required, such as sharing links or server-side redirection.

- **Full URL Retrieval (`router.page.full_raw_path`)**:
    - **Functionality**: Retrieves the entire URL of the current page as seen in the browser, including the protocol (http/https), domain, and any path or query parameters.
    - **Use Case**: Ideal for functionalities that require the absolute URL, such as link sharing, redirecting to other pages, or when building URLs for server-side processing.
    - **Example Usage**: This is especially useful when generating URLs for external use, where the complete path is necessary.In a development environment, this might return something like ```http://localhost:3000/about-us```

#### Example: Retrieving the Complete URL

```python
class State(xt.State):
    @xt.var
    def get_full_url(self) -> str:
        # Retrieve the full URL of the current page
        return self.router.page.full_raw_path
```

In this example, `get_full_url` is a method that returns the full URL of the current page. This is particularly useful for operations that depend on the entire URL.

#### Fetching the Client's IP Address

The client's IP address can be a critical piece of information for various functionalities in web applications, such as for security auditing, geo-targeting content, or tracking user activity.

- **IP Address Retrieval (`router.session.client_ip`)**:
    - **Functionality**: Allows you to obtain the IP address of the client associated with the current state.
    - **Use Case**: Useful for logging client activity, implementing geo-restrictions, personalizing content based on user location, or for additional security measures.
    - **Example Context**: In a chat application, you might want to log the IP addresses of users for security and moderation purposes.

#### Example: IP Address Retrieval

```python
class State(xt.State):
    def log_client_activity(self):
        # Obtain and log the client's IP address
        client_ip = self.router.session.client_ip
        print("Client IP Address:", client_ip)
        # Additional logic based on the client's IP address
```

Here, `log_client_activity` is a method that retrieves and logs the client's IP address. This can be utilized for various purposes, from basic logging to more complex user interaction based on geographical location.


### Page Metadata

Metadata includes titles, descriptions, visual previews (through images), and additional meta tags. These elements collectively contribute to a more informative and appealing web page, both in terms of SEO (Search Engine Optimization) and user engagement.

#### Key metadata attributes you can use in Nextpy:

| Attribute   | Purpose                                                                                      | Impact                                                                                                           | Example Usage                                            |
|-------------|----------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------|
| `title`     | Sets the title of the web page, visible in browser tabs and used by search engines.          | Crucial for SEO, helps users quickly identify the page content.                                                  | `title="Home Page - My Nextpy App"`                      |
| `image`     | Specifies a visual identifier or favicon for the page, often used in social media sharing.   | Enhances visual appeal and recognition, increases engagement when shared on social media.                        | `image="/assets/favicon.ico"`                            |
| `description` | Provides a brief summary of the page's content, used by search engines for snippets.          | Improves click-through rates from search results, offers users a quick understanding of the page.                | `description="Learn about our latest Nextpy projects"`   |
| `meta`      | Allows for additional meta tags, containing custom information or instructions for the page. | Enables specification of page characteristics, controls indexing, or provides data for analytical tools.        | `meta=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}]` |

#### Example


```python

@xt.page(
    title="The Enchanted App",
    description="Journey through a magical Nextpy creation",
    image="/enchanted-forest.jpg",
    meta=[{"name": "color_scheme", "content": "forest_green"}]
)
def enchanted_page():
    return xt.text("Welcome to the Enchanted App")

```
#### Additional metadata with meta attribute:

Here are the additional metadata options you can use in Nextpy with the `meta` attribute:

| Meta Attribute         | Description                                              | Example Usage                                                                      |
|------------------------|----------------------------------------------------------|------------------------------------------------------------------------------------|
| Viewport Settings      | Defines the viewport characteristics for responsive design. | `{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}`        |
| Character Set          | Specifies the character encoding for the web page.        | `{"charset": "UTF-8"}`                                                            |
| Keywords               | Provides search engines with specific keywords related to the page content. | `{"name": "keywords", "content": "Nextpy, web development, programming"}`         |
| Author                 | Denotes the author of the webpage content.                | `{"name": "author", "content": "Jane Doe"}`                                       |
| Refresh                | Controls how the page should refresh, such as automatic redirection after a specified time. | `{"http-equiv": "refresh", "content": "30;url=https://example.com"}`              |
| Custom Metadata       | Allows the definition of any custom metadata relevant to your application. | `{"name": "custom_meta", "content": "Custom Value"}`                              |


**Page Load Events**
- The page load events can be used to initialize and prepare your app's state right when a page is first loaded. 
- For example,fetching information from an API, setting up initial state variables, or performing any setup tasks that are necessary before the user interacts with the page.
- You can define multiple functions or a series of steps within a single function to handle various initialization tasks. This flexibility allows for a clean and organized approach to handling page-specific preparations.

**Example**

```python

import nextpy as xt
from typing import Dict, Any

def fetch_data():
    return {"message": "Welcome to Nextpy!", "data": "Sample data fetched"}

class State(xt.State):
    data: Dict[str, Any] = {}

    def function_called_on_load(self):
        self.data = fetch_data()

# Define the page with on_load event
@xt.page(on_load=State.function_called_on_load)
def index():
    # Displaying the fetched data on the page
    return xt.text(f"Hello, Page load! Data: {State.data['message']}")

app = xt.App()
app.add_page(index)

```
