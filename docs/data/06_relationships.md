### Understanding Relationships

In databases, relationships are crucial for linking data between different tables. `xt.Model` provides a powerful way to define and manage these relationships, ensuring data integrity and enabling efficient queries. In this tutorial, we'll explore how to work with relationships using product examples, replacing the user examples from the original context.

---

**Foreign Key Relationships**

A foreign key is a column in one table that references the primary key of another table. It creates a connection between the two tables, allowing you to navigate and query related data.

Imagine products and categories in a store. Each product belongs to a single category, and the product table would have a `category_id` foreign key referencing the `id` of the category table.

#### 2. Defining Foreign Key Relationships in SQLModel:

Use the `foreign_key` argument within the `Field` definition for the referencing column:

```python
import sqlmodel
import nextpy as xt

class Product(xt.Model, table=True):
    name: str
    price: float
    category_id: int = sqlmodel.Field(foreign_key="category.id")
```

This specifies that the `category_id` in the `Product` table refers to the `id` column in the `Category` table.

#### 3. Relationship Attributes and Back Population:

SQLModel uses relationship attributes to access related objects.

Add a relationship attribute in the referencing model, pointing to the related model:

```python
class Product(xt.Model, table=True):
    # ... other fields ...
    category: Optional["Category"] = sqlmodel.Relationship(back_populates="products")
```

This creates a `category` attribute in the `Product` model, allowing you to easily access the associated category object.

Use `back_populates` to create a corresponding attribute in the related model:

```python
class Category(xt.Model, table=True):
    name: str
    # Relationship to products
    products: List[Product] = sqlmodel.Relationship(back_populates="category")
```

Now, you can access products from a category and vice versa:

```python
product = session.get(Product, 1)
category = product.category
for product in category.products:
    print(product.name)
```

#### Complex example

In this setup, `User` and `Product` are related through the `Review` model. Each `User` can have multiple reviews, and each `Product` can also have multiple reviews.

```python
from typing import List, Optional
import sqlmodel
import nextpy as xt

class User(xt.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    username: str
    email: str

    # Relationships
    reviews: List["Review"] = sqlmodel.Relationship(back_populates="author")

class Product(xt.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    name: str
    price: float
    description: Optional[str] = None

    # Relationships
    reviews: List["Review"] = sqlmodel.Relationship(back_populates="product")

class Review(xt.Model, table=True):
    id: Optional[int] = sqlmodel.Field(default=None, primary_key=True)
    product_id: int = sqlmodel.Field(default=None, foreign_key="product.id")
    author_id: int = sqlmodel.Field(default=None, foreign_key="user.id")
    content: str

    # Relationships
    product: Optional[Product] = sqlmodel.Relationship(back_populates="reviews")
    author: Optional[User] = sqlmodel.Relationship(back_populates="reviews")
```

#### Inserting Linked Objects

To insert a new `Review` for a `Product` by a `User`, you would create a form-handling state class like this:

```python
class ReviewProductForm(State):
    author: User  # Assume the author is already stored in the state.

    def review_product(self, form_data: dict[str, str]):
        with xt.session() as session:
            product = session.get(
                Product, int(form_data["product_id"])
            )
            review = Review(
                content=form_data["content"],
                product_id=product.id,
                author_id=self.author.id,
            )
            session.add(review)
            session.commit()
```

---

## Understanding How Relationships Are Dereferenced

When you have two tables connected by a relationship, like a list of books and their authors, you might want to access the author of a book or all books written by a certain author. In SQLModel, this is done through something called "relationship attributes."

By default, SQLModel uses what's called "lazy loading" for these relationships. This means that the related data (like the author's information) isn't loaded from the database until you actually ask for it in your code. Think of it like a book on a shelf; the book (author's information) isn't taken off the shelf (loaded from the database) until you decide to pick it up (access it in your code).

While lazy loading is simple and usually works fine when you're dealing with one item at a time (like looking up a single author), it can slow things down if you're working with lots of items (like loading all authors for a long list of books).

To make things more efficient, especially when dealing with lots of data, SQLModel offers different ways to load this related data:

1. **"joined" or joinload**: This method grabs all the related data you need in one go. It's like telling a librarian to bring you all the books by a certain author along with the author's biography in one trip.
2. **"subquery" or subqueryload**: Similar to joinload, this method also gets all the related data in one go but does it in a slightly different technical way. It's like asking for the same books and biography as before, but this time the librarian checks a special index first before bringing them to you.
3. **"selectin" or selectinload**: This method is a bit different. Instead of getting everything in one go, it first makes a list of the specific things it needs and then gets them all at once. Imagine you gave the librarian a list of book titles, and she brings all those books to you in a single basket. There are also options to avoid loading the related data entirely:
   - **"raise"**: This tells SQLModel to give you an error if you try to access the related data. It's like putting a "do not touch" sign on the bookshelf.
   - **"noload"**: This tells SQLModel to ignore the related data completely. It's as if the books aren't even on the shelf to begin with.

Choosing the right loading method depends on what you're doing with the data. For most cases, it's often best to stick with the default lazy loading until you notice things are getting slow, and then explore other options.

### Querying Linked Objects

To query the `Product` table and include all associated `Review` and `User` objects upfront, you use the `.options` interface to specify `selectinload` for the required relationships:

```python
import sqlalchemy

class ProductState(State):
    products: List[Product]

    def load_products_with_reviews(self):
        with xt.session() as session:
            self.products = session

.exec(
                sqlmodel.select(Product).options(
                    sqlalchemy.orm.selectinload(Product.reviews).selectinload(Review.author)
                )
            ).all()
```

This code loads all `Product` objects with their `reviews` and the `author` of each review in a single query, preventing the N+1 query problem.

### Specifying the Loading Mechanism on the Relationship

You can also specify the loading mechanism directly on the relationship within the `Product` model:

```python
class Product(xt.Model, table=True):
    # ... other fields ...

    reviews: Optional[List["Review"]] = sqlmodel.Relationship(
        back_populates="product",
        sa_relationship_kwargs={"lazy": "selectin"},
    )
```
By setting `sa_relationship_kwargs={"lazy": "selectin"}`, you specify that whenever you query for `Product` objects, SQLModel will automatically use the `selectin` loading strategy for the `reviews` relationship.
