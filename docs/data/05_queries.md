**Key Concepts:**

- **Query:** A request to retrieve, insert, update, or delete data from a database.
- **Session:** A temporary workspace for interacting with the database, ensuring data consistency and preventing errors.
- **Model:** A blueprint for how your data is organized in the database (like a Product model with id, name, price).
- **CRUD Operations:** Create, Read, Update, Delete operations performed on data through sessions.

### Sessions

Sessions serve as essential workspaces for interacting with your database. They ensure data consistency and prevent potential issues during database operations.

### Why Sessions Matter

- **Connection Management:** Sessions facilitate the connection to your database, handling the opening and closing of connections seamlessly.
- **Concurrency Control:** They help manage concurrency, ensuring that multiple processes can access the database without conflicts or data corruption.
- **Transactional Integrity:** Sessions ensure that your database operations are treated as transactions. This means either all operations within a session are successfully executed or none are, maintaining data integrity.

### Using Sessions in Nextpy

To execute any query in Nextpy, you first need to create a session. 

**Key Concepts:**

- **Session Creation:** To initiate a session, use the `xt.session()` context manager. This creates a temporary workspace for your database interactions.
- **Committing Changes:** To commit changes to the database, use `session.commit()`. This  finalizes the transaction and saves the modifications.

Note- **If `session.commit()` is not called, the changes will be rolled back and not persisted to the database.**

- **Explicit** **Rollbacks:** If you need to undo changes within a session, use `session.rollback()`. This reverts the operations without affecting the database.
- **Automatic Closure:** Sessions automatically close when the code block within the `with` statement ends, ensuring proper resource management.

### Example: Creating and Using a Session

Here's a simple example demonstrating how to open and use a session in a Nextpy application:

```python
with xt.session() as session:
    # Assuming a Product model is already defined
    new_product = Product(name="Nextpy Gadget", price=49.99)
    session.add(new_product)
    session.commit()

```

**Explanation:**

1. The `with xt.session() as session:` statement creates a session context.
2. A new product object is created within the session.
3. The `session.add(new_product)` line schedules the addition of the product to the database.
4. The `session.commit()` command executes the transaction, saving the product to the database permanently.

**Remember:** Always initiate and commit sessions appropriately to ensure data integrity and consistency in your Nextpy applications.

### Let’s define product model

- **Model Definition**: Think of a model as a blueprint of your data. Here's how you define a `Product`:
    
    ```python
    class Product(xt.Model, table=True):
        id: int
        name: str
        price: float
    
    ```
    
    - `id`, `name`, and `price` are attributes of each product.

### **Adding Data (Create)**

- **Adding a New Product**: Think of this like adding a new row to your product table.
    
    ```python
    class AddProduct(State):
        name: str
        price: float
    
        def add_product(self):
            with xt.session() as session:
                new_product = Product(name=self.name, price=self.price)
                session.add(new_product)
                session.commit()
    
    ```
    
    - `session.add(new_product)` tells Nextpy, "Please add this new product to the database."

### **Retrieving Data (Read)**

- **Fetching Products with Specific Criteria**: To get data from your database, you use a query. For example, finding products by name:
    
    ```python
    class QueryProduct(State):
        search_term: str
        products: list[Product]
    
        def get_products(self):
            with xt.session() as session:
                self.products = session.exec(
                    Product.select().where(Product.name.contains(self.search_term))
                ).all()
    
    ```
    
    - `Product.select().where()` is like asking, "Can you show me products that have these characteristics?"

### **Modifying Data (Update)**

- **Modifying an Existing Product**: Sometimes, you need to update details of an existing product.
    
    ```python
    class UpdateProduct(State):
        product_id: int
        new_price: float
    
        def update_product_price(self):
            with xt.session() as session:
                product = session.exec(
                    Product.select().where(Product.id == self.product_id)
                ).first()
                product.price = self.new_price
                session.add(product)
                session.commit()
    
    ```
    
    - This is like saying, "I found this product; now, let's change its price."

### **Deleting Data (Delete)**

- **Deleting a Product**: Removing a product is straightforward but permanent.
    
    ```python
    class DeleteProduct(State):
        product_id: int
    
        def delete_product(self):
            with xt.session() as session:
                product = session.exec(
                    Product.select().where(Product.id == self.product_id)
                ).first()
                session.delete(product)
                session.commit()
    
    ```
    
    - `session.delete(product)` means "Remove this product from the database."

**Understanding ORM Object Lifecycle**

**Objects and Sessions: A Bound Relationship**

- Objects retrieved from database queries are tightly coupled with the session that created them.
- Using these objects outside of their associated session can lead to unexpected behavior and potential errors.

**Automatic Updates: Not Always Comprehensive**

- After performing CRUD (Create, Read, Update, Delete) operations within a session, not all object attributes are automatically updated.
- Accessing certain attributes might trigger additional queries to refresh the object's state, potentially impacting performance.

**Refreshing Objects for Accurate Data**

- To ensure you're working with the latest data, explicitly refresh objects after modifications using the `session.refresh(object)` method. This updates the object's state with the most recent information from the database.
- **Retrieving Autogenerated IDs:** After adding a product and committing the transaction, the `session.refresh(product)` method ensures you have access to the product's autogenerated ID, even if it wasn't provided in the initial form data.

Example

```python
# Assuming a Product model with an auto-incrementing 'id' field
class AddProductForm(State):
    product: Product | None = None

    def add_product(self, product_data: dict[str, str]):
        with xt.session() as session:
            self.product = Product(**product_data)
            session.add(self.product)
            session.commit()
            session.refresh(self.product)  # Now you can access the generated 'id'

        # Accessing the generated ID:
        print(self.product.id)  # Assuming you want to use the ID outside the session

```

- **Working with Products Across Sessions:** If you need to modify or use a product object in a separate session, add it to the new session using `session.add(product)`. This associates the object with the new session, ensuring proper tracking of changes.

```python
class UpdateProductForm(State):
    product: Product | None = None

    def update_product(self, updated_data: dict[str, str]):
        with xt.session() as session:
            if self.product is None:
                return
            session.add(self.product)  # Add the product to the new session
            self.product.set(**updated_data)
            session.commit()
            session.refresh(self.product)

```

**Key Reminders:**

- **Refreshing for Consistency:** Always refresh product objects after modifications, even within the same session, to guarantee you're working with the latest data.
- **Stale Object Handling:** Refresh objects before using them outside of their original session to prevent stale object exceptions and ensure data accuracy.

### Direct SQL Execution: When and How

- **Using Raw SQL**: While ORMs simplify interactions, sometimes you need the precision of raw SQL.
    - **Safety First**: Always use parameterized queries (like `sqlalchemy.text`) to prevent SQL injection attacks.
    - Example: Inserting a product using raw SQL.
    

## Using Raw **SQL Queries**

While our ORMs offer a convenient and object-oriented way to interact with your database, sometimes you might need to venture into the raw power of SQL queries. 

**When to Opt for Raw SQL:**

ORMs are great for most CRUD operations and simple queries. However, raw SQL is quite helpful in specific scenarios:

- **Complex Joins:** When dealing with intricate relationships between tables, raw SQL joins can offer greater flexibility and control compared to ORM relationships.
- **Database-Specific Features:** Certain features unique to your database engine might not be readily available through ORMs. Raw SQL allows you to leverage these functionalities directly.
- **Performance Optimization:** In some cases, carefully crafted raw SQL queries can be more efficient than their ORM counterparts.

**Security Precautions**

While powerful, raw SQL demands care due to potential security vulnerabilities. Here's how to ensure safe exploration:

- **Never use string formatting to build queries:** This opens the door to SQL injection attacks, where malicious users can inject harmful code into your query.
- **Embrace Parameterized Queries:** Instead of building strings, use placeholders with `sqlalchemy.text` and bind your data separately. This ensures safe and clean query execution.
- **Escape User Input:** Always sanitize user input before using it in raw SQL queries to prevent manipulation attempts.

**Example of Raw SQL** 

**1. Inserting a Product with Parameterized Query:**

```python
import sqlalchemy
import nextpy as xt

class State(xt.State):
    def insert_product(self, product_name, price):
        with xt.session() as session:
            session.execute(
                sqlalchemy.text(
                    "INSERT INTO product (name, price) "
                    "VALUES (:name, :price)"
                ),
                {"name": product_name, "price": price},
            )
            session.commit()
```

**2. Retrieving Product Data with Custom Query:**

```python
import nextpy as xt

class State(xt.State):
    @xt.var
    def get_electronics_products(self) -> list[dict]:
        with xt.session() as session:
            raw_products = session.execute(
                sqlalchemy.text(
                    "SELECT id, name, price, description "
                    "FROM product "
                    "WHERE category = 'Electronics' "
                    "ORDER BY price ASC"
                )
            ).all()
            return [
                {"id": row[0], "name": row[1], "price": row[2], "description": row[3]}
                for row in raw_products
            ]
```

**3. Updating a Product Price with Raw SQL:**

```python
import nextpy as xt

class State(xt.State):
    def update_product_price(self, product_id, new_price):
        with xt.session() as session:
            session.execute(
                sqlalchemy.text(
                    "UPDATE product "
                    "SET price = :new_price "
                    "WHERE id = :product_id"
                ),
                {"new_price": new_price, "product_id": product_id},
            )
            session.commit()
```

**Notes:**

- Ensure you have imported `sqlalchemy` where necessary.
- Use the `@xt.var` decorator when a method is meant to be a variable (property) and does not alter the state of the database.
- Enclose SQL commands within `sqlalchemy.text()` for parameterized queries.
- Use `session.commit()` after executing queries that modify the database.
- Include the method calls within the class `State`.
- The `with xt.session() as session:` context manager should be placed inside the methods.
- Ensure you have `session.execute().all()` when expecting multiple rows from the query.
- Make sure to return the formatted result in methods that retrieve data.
