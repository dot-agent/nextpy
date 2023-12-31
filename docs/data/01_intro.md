# Introduction to Database

Nextpy’s data module empowers your Python applications with database capabilities, simplifying the way you store and manage data. This guide walks you through the essentials, catering to both beginners and experienced users.

## Key Concepts for Beginners

- **ORM (Object-Relational Mapping):** A technique that bridges the gap between your Python application and a database, allowing them to communicate effectively. Think of it as a translator that converts data between their different languages.
- **SQLModel:** A Python library built on top of SQLAlchemy, designed to make database interactions more intuitive and Pythonic. It provides a clear way to define your data models and interact with the database.
- **SQLite:** A lightweight, file-based database system that's easy to set up and use. It's a great option for simpler applications or prototyping.
- **SQLAlchemy:** A powerful Python toolkit that simplifies database interactions, handling a wide range of tasks and making database management more efficient.

## Connecting to Your Database

1. **Default SQLite Setup:**
    - Nextpy comes with SQLite ready to go. To use it, simply configure the database URL in your `xtconfig.py` file:

    ```python
    config = xt.Config(
        app_name="my_app",
        db_url="sqlite:///mydatabase.db"  # Path to your SQLite database file
    )
    ```

2. **Connecting to Other Databases:**
    - To use a different SQL database like MySQL or PostgreSQL, update the `db_url` in `xtconfig.py` with the appropriate connection string. Find supported formats in the SQLAlchemy documentation.

## Defining Your Data Models

- Create Python classes that inherit from `xt.Model` to represent tables in your database:

```python
class Product(xt.Model, table=True):
    id: int
    name: str
    price: float
```

## Managing Database Changes with Migrations

- Nextpy uses Alembic to track and manage changes to your database schema:
    - **Initialization:** Run `nextpy db init` to set up Alembic in your project.
    - **Creating Migrations:** After modifying models, use `nextpy db makemigrations` to create a migration script.
    - **Applying Migrations:** Run `nextpy db migrate` to update your database structure.

## Performing Database Operations

- Use `xt.session()` to interact with the database:

```python
with xt.session() as session:
    new_product = Product(id=1, name="Widget", price=19.99)
    session.add(new_product)
    session.commit()
```

## Additional Resources

- **SQLModel Documentation:** [https://sqlmodel.tiangolo.com/](https://sqlmodel.tiangolo.com/)
- **SQLite Documentation:** [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html)
- **SQLAlchemy Documentation:** [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
