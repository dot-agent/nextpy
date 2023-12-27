## State Object Utilities

Nextpy's state object is equipped with various methods and attributes that are crucial for understanding and managing the state of your application, especially in regards to user interactions and data management.

### The `router` Attribute

The `router` attribute in the state object  provides comprehensive details about the current page and user session. It's a crucial tool for understanding how users interact with your application and managing their experience effectively.

### Detailed Breakdown of `router`

1. **Page Information (`router.page`)**:
    - `host`: Represents the hostname and port where the current page is being served. This is essential for constructing absolute URLs or understanding the deployment environment.
    - `path`: This is the path of the current page. In the case of dynamic pages, it includes the slug, offering insights into the specific page the user is viewing.
    - `raw_path`: Reflects the path as shown in the browser. It includes query parameters and dynamic values, providing a more comprehensive view of the user's current location in the app.
    - `full_path`: A combination of `host` and `path`, giving the complete URL of the current page. Useful for redirects or generating links.
    - `full_raw_path`: Similar to `full_path`, but includes query parameters and dynamic values, mirroring the URL as seen in the browser.
    - `params`: Contains a dictionary of all query parameters associated with the current request. This is useful for processing user inputs and customizing page content based on these parameters.
2. **Session Information (`router.session`)**:
    - `client_token`: A unique identifier for each browser tab, allowing you to track and manage individual user sessions and tab-specific states.
    - `session_id`: This unique ID is tied to the client's WebSocket connection, facilitating real-time communication and state management.
    - `client_ip`: The IP address of the client accessing your application. While multiple users might share the same IP, this information can be useful for analytics, security checks, or location-based customization.
3. **WebSocket Headers (`router.headers`)**:
    - This offers a selection of the most commonly used headers associated with the WebSocket connection. These headers typically remain constant unless the connection is re-established, like during a page refresh. Understanding these headers can be crucial for debugging, security, and ensuring optimal performance of your application.

### Practical Implications

The `router` attribute effectively serves as a navigation and session management tool within Nextpy apps. By providing detailed insights into the user's current state and session, it allows developers to create more dynamic, responsive, and user-tailored experiences. Whether it's for routing decisions, customizing content, security measures, or analytics, the `router` attribute is an indispensable part of the Nextpy toolkit.

### Sample Router Attribute Values:

```
Example router.page.host:            <https://nextpy.org>
Example router.page.path:            /docs/state/utility-methods
Example router.page.raw_path:        /docs/state/utility-methods/
Example router.page.full_path:       <https://nextpy.org/docs/state/utility-methods>
Example router.page.full_raw_path:   <https://nextpy.org/docs/state/utility-methods/>
Example router.page.params:          {}
Example router.session.client_token: 18be02e2-277e-4bfa-cdc9-2d8397564b8e
Example router.session.session_id:   PUgmmhoyziaB1lPFAC36
Example router.session.client_ip:    127.0.0.1
Example router.headers.host:         prod-nextpy-org.fly.dev

```

### Additional Utility Methods

Beyond `router`, the state object includes other methods for state manipulation:

- **`reset`**: Resets all `Var` instances to their default values.
- **`get_value`**: Retrieves a `Var`'s value without tracking changes, useful for serialization.
- **`dict`**: Converts all state `Var` instances to a dictionary, used for initial page load hydration.

### Special Internal Attributes

Nextpy also utilizes specific internal attributes:

- **`dirty_vars`**: A set of `Var` names that have changed since the last update, helping Nextpy decide which `Var` instances to update on the client side post-event.
