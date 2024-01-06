# Var

In Nextpy, variables (Vars) are the elements that might change as your app runs. Here's a breakdown of the different types of variables in Nextpy and their uses:

### Base **Vars**

**Base Vars** are the fundamental building blocks of your app's state, storing data that can change, such as product names or prices. They are defined within your state class like regular variables and can have default values or specific data types.

1. **Definition as State Class Fields**: Base variables are declared as fields within the state class.
2. **Default Values and Type Annotations**: They can be initialized with default values. If no default value is provided, a type annotation is mandatory to define the variable's data type.
3. **Type Annotations for State Variables**: Nextpy uses type annotations to ascertain the types of state variables during the compilation process, ensuring type safety and consistency.

### Example Implementation

In this example, product_name and product_price are base variables representing the name and price of a product. This can be dynamically updated based on user interaction or other processes in the application.

```python
import nextpy as xt

class ProductState(xt.State):
    product_name: str = "Widget X"
    product_price: str = "$25"

def product_example():
    return xt.stat_group(
        xt.stat(
            xt.stat_label(ProductState.product_name),
            xt.stat_number(ProductState.product_price),
            xt.stat_help_text(
                xt.stat_arrow(type_="increase"),
                "popular choice",
            ),
        ),
    )

def index():
    return xt.fragment(
        product_example(),
    )

app = xt.App()
app.add_page(index)

```

### JSON Serialization of Vars

- **Communication Between Frontend and Backend**: Base variables are pivotal in the exchange of data between the frontend and backend.
- **JSON Serializable Data Types**: They must be JSON serializable, which includes primitive Python types, Plotly figures, Pandas dataframes, or custom-defined types.

### Computed Variables

**Computed Vars** are special variables that calculate their own values based on other variables. They automatically update when their dependencies change, such as calculating a total price. They are defined as methods within your state class using the `@xt.var` decorator.

1. **Dynamic Recalculation**: Computed variables are automatically updated whenever there is a change in the state variables they depend on.
2. **Defined as State Class Methods**: They are implemented as methods within the state class and are decorated with `@xt.var`.
3. **Dependence on State Variables**: Their values are derived from other properties in the state.

### Example Implementation

Here, capitalized_description is a computed variable that always holds the capitalized version of description.

```python
import nextpy as xt

class DescriptionState(xt.State):
    description: str = "compact and efficient"

    @xt.var
    def capitalized_description(self) -> str:
        # This will be recomputed whenever `description` changes.
        return self.description.capitalize()

def description_example():
    return xt.vstack(
        xt.heading(DescriptionState.capitalized_description),
        xt.input(
            on_blur=DescriptionState.set_description,
            placeholder="Update description...",
        ),
    )

```

### Best Practices

- **Type Annotations**: Always use type annotations for computed variables. This practice enhances code readability and maintainability.

### Practical Use Cases

- **Data Formatting**: Ideal for formatting or transforming data for display purposes.
- **Derived Properties**: Useful for creating properties that are derived from one or more state variables.
- **Real-time Calculations**: Efficient for calculations that need to be updated in real-time based on user interactions or other state changes.

### Cached Variables

**Cached Vars** are optimized computed variables that only recalculate when specific dependencies change. They are useful for complex calculations to save processing power. They are marked with the `@xt.cached_var` decorator in your state class.

1. **Efficient Recomputation**: Unlike regular computed variables, cached variables are not recalculated every time the state updates, but only when their dependent variables change.
2. **Optimization for Expensive Computations**: Ideal for scenarios where the computation is resource-intensive.
3. **Selective Updates**: Provides a way to update only specific parts of the state, based on changes to certain variables.

### Example Implementation

In this example, the cached variables last_positive_review_update and last_negative_review_update are updated only when their respective review counts change:

```python
import nextpy as xt
import time

class ReviewState(xt.State):
    positive_reviews: int = 0
    negative_reviews: int = 0

    @xt.var
    def last_update_time(self) -> str:
        # Updated anytime the state is updated.
        return time.strftime("%H:%M:%S")

    def add_positive_review(self):
        self.positive_reviews += 1

    @xt.cached_var
    def last_positive_review_update(self) -> str:
        # Updated only when `positive_reviews` changes.
        return f"Positive Reviews: {self.positive_reviews} at {time.strftime('%H:%M:%S')}"

    def add_negative_review(self):
        self.negative_reviews += 1

    @xt.cached_var
    def last_negative_review_update(self) -> str:
        # Updated only when `negative_reviews` changes.
        return f"Negative Reviews: {self.negative_reviews} at {time.strftime('%H:%M:%S')}"

def review_example():
    return xt.vstack(
        xt.text(f"Last Updated at: {ReviewState.last_update_time}"),
        xt.text(ReviewState.last_positive_review_update),
        xt.text(ReviewState.last_negative_review_update),
        xt.hstack(
            xt.button("Add Positive Review", on_click=ReviewState.add_positive_review),
            xt.button("Add Negative Review", on_click=ReviewState.add_negative_review),
        ),
    )

```

### Practical Use Cases

- **Performance Optimization**: Use in scenarios where the computation is heavy and doesn't need to be updated with every state change.
- **Selective State Updates**: Ideal for situations where only specific parts of the state need frequent updates.
- **Resource Management**: Reduces the load on both the server and client by minimizing unnecessary recalculations.

### Backend-only **Vars**

**Backend-only Vars** are variables that remain hidden on the server, never sent to the user's browser. They are used for sensitive data or large datasets that are not needed for direct client-side rendering. They are identified by a leading underscore in their names (e.g., `_secret_data`).

### Key Characteristics:

1. **Non-Synchronized**: These variables are not sent to the frontend, reducing unnecessary network traffic and enhancing performance.
2. **Data Security**: Ideal for handling sensitive information that should not be exposed to the client-side.
3. **Flexibility in Data Types**: Unlike standard variables, backend-only variables do not require JSON serialization. However, they need to be cloudpickle-able for compatibility with Redis in production environments.
4. **Efficient Data Handling**: Useful for storing large data structures or session-specific information that doesn’t need to be rendered directly on the frontend.

### Example Implementation

In this example, _inventory_data is a backend-only variable storing the quantities of each product in the inventory. The frontend displays paginated views of this inventory, reducing the amount of data transferred between backend and frontend. The restock_inventory method simulates adding new stock to the inventory, showcasing the dynamic nature of backend-only variables.

```python
import numpy as np
import nextpy as xt
import random

class InventoryState(xt.State):
    _inventory_data: np.ndarray = np.array([random.randint(0, 500) for _ in range(100)])
    page_offset: int = 0
    page_limit: int = 10

    @xt.cached_var
    def inventory_page(self) -> list[int]:
        return [
            int(quantity)  # explicit cast to int
            for quantity in self._inventory_data[
                self.page_offset : self.page_offset + self.page_limit
            ]
        ]

    @xt.cached_var
    def current_page_number(self) -> int:
        return (
            (self.page_offset // self.page_limit) + 1
            + (1 if self.page_offset % self.page_limit else 0)
        )

    @xt.cached_var
    def total_inventory_pages(self) -> int:
        return len(self._inventory_data) // self.page_limit + (
            1 if len(self._inventory_data) % self.page_limit else 0
        )

    def previous_page(self):
        self.page_offset = max(self.page_offset - self.page_limit, 0)

    def next_page(self):
        if self.page_offset + self.page_limit < len(self._inventory_data):
            self.page_offset += self.page_limit

    def restock_inventory(self):
        self._inventory_data = np.append(
            self._inventory_data,
            [random.randint(0, 500) for _ in range(random.randint(0, 100))]
        )

def inventory_example():
    return xt.vstack(
        xt.hstack(
            xt.button("Prev", on_click=InventoryState.previous_page),
            xt.text(f"Page {InventoryState.current_page_number} / {InventoryState.total_inventory_pages}"),
            xt.button("Next", on_click=InventoryState.next_page),
            xt.text("Page Size"),
            xt.number_input(
                width="5em",
                value=InventoryState.page_limit,
                on_change=InventoryState.set_page_limit,
            ),
            xt.button("Restock Inventory", on_click=InventoryState.restock_inventory),
        ),
        xt.list(
            xt.foreach(
                InventoryState.inventory_page,
                lambda quantity, index: xt.text(
                    f"Inventory Item[{index + InventoryState.page_offset}] = {quantity}"
                ),
            ),
        ),
    )

```

### Practical Use Cases

- **Session-Specific Data**: Manage data related to user sessions without exposing it to the client-side.
- **Sensitive Information**: Securely handle sensitive data like API keys or user credentials.
- **Data Pagination**: Efficiently manage large datasets by storing them on the backend and sending only necessary portions to the frontend.

### Client-Storage Variables

**Client-Storage Vars** are variables that persist user-specific data across browser sessions, such as login information or preferences. You can choose between cookie (`xt.Cookie`) or local storage (`xt.LocalStorage`) options. They behave like regular string variables with the added benefit of persistence.

### Key Features:

1. **Persistence Across Sessions**: Data stored in client-storage variables remains accessible across different browser sessions, providing a continuous user experience.
2. **Seamless Integration**: These variables integrate smoothly into the Nextpy framework, behaving much like standard string variables but with enhanced capabilities for data persistence.
3. **Flexibility in Storage**: Depending on your requirements, you can choose between `xt.Cookie` for cookie storage and `xt.LocalStorage` for storing data in the browser's local storage.
4. **Customizable Key Names**: While the default key name for these variables is derived from the variable's name, you have the option to set a custom key name using the `name` parameter.

### Implementing Client-Storage Variables

Here's a practical example to illustrate the implementation of client-storage variables in Nextpy:

```python
import nextpy as xt

class CustomerPreferenceState(xt.State):
    favorite_product: str = xt.Cookie("Widget X")
    recently_viewed: str = xt.LocalStorage("Widget X")
    custom_preference: str = xt.Cookie(name="PreferredColor", max_age=3600)

def preference_example():
    return xt.vstack(
        xt.hstack(
            xt.text("Favorite Product"),
            xt.input(
                value=CustomerPreferenceState.favorite_product,
                on_change=CustomerPreferenceState.set_favorite_product,
            ),
        ),
        xt.hstack(
            xt.text("Recently Viewed"),
            xt.input(
                value=CustomerPreferenceState.recently_viewed,
                on_change=CustomerPreferenceState.set_recently_viewed,
            ),
        ),
        xt.hstack(
            xt.text("Custom Preference"),
            xt.input(
                value=CustomerPreferenceState.custom_preference,
                on_change=CustomerPreferenceState.set_custom_preference,
            ),
        ),
    )

```

### Practical Use Cases

- **User Preferences**: Store and retrieve user settings like theme preferences or layout choices.
- **Session Management**: Maintain session tokens or authentication cookies securely.
- **Form Data**: Keep form inputs intact when users navigate away and return to the page.
