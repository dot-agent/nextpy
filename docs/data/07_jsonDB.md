# JsonDatabase

## Introduction
The `JsonDatabase` class provides a simple, JSON file-based database system. It's particularly useful for small projects or situations where a full-scale database system is unnecessary. This guide will introduce you to the `JsonDatabase` class, explaining its core functionality and showing you how to use it with simple examples.

### Prerequisites
- Basic understanding of Python programming.
- Familiarity with classes and exception handling in Python.
- Knowledge of JSON file format.

## JsonDatabase Class Overview

### Key Features
- **CRUD Operations**: Create, Read, Update, Delete operations for data.
- **JSON File Storage**: Data is stored in a JSON file, easy to view and edit.
- **SQLModel Integration**: Utilizes SQLModel for data validation and schema definition.
- **Concurrency Handling**: Uses `FileLock` to handle concurrent access to the JSON file.

### Core Methods
- `add(instance: T) -> T`: Adds a new data instance.
- `query(**kwargs) -> List[T]`: Queries data based on provided parameters.
- `get(id_value: int) -> Optional[T]`: Retrieves an instance by ID.
- `delete(id_value: int) -> None`: Deletes an instance by ID.
- `update(id_value: int, new_data: Dict[str, Any]) -> None`: Updates an instance by ID.

### Exception Handling
- Custom exceptions like `IdNotFoundError`, `DataNotFoundError`, and `SchemaError` for better error management.

## Getting Started with JsonDatabase

### Setting Up
First, ensure you have the `sqlmodel` and `filelock` packages installed:
```bash
pip install sqlmodel filelock
```

### Defining a Model
Let's start by defining a simple model using SQLModel:

```python
from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str
```

### Creating the Database
Now, create an instance of `JsonDatabase` using the `User` model:

```python
db = JsonDatabase('users.json', model=User)
```

### Basic Operations
#### Adding Data
To add a new user:

```python
new_user = User(username="johndoe", email="john@example.com", password="securepassword")
db.add(new_user)
```

#### Querying Data
To find users by username:

```python
users = db.query(username="johndoe")
print(users)
```

#### Updating Data
To update a user's password:

```python
db.update(new_user.id, {"password": "newstrongpassword"})
```

#### Deleting Data
To delete a user:

```python
db.delete(new_user.id)
```

### Error Handling
It's important to handle errors such as `IdNotFoundError`. Here's an example:

```python
try:
    db.delete(123)  # Assuming 123 is a non-existent ID
except IdNotFoundError as e:
    print(e)
```


The `JsonDatabase` class provides a straightforward way to implement a JSON-based database in Python, especially useful for small-scale projects or for learning purposes. By following the examples provided, you can perform basic CRUD operations and handle exceptions effectively.

Remember, while `JsonDatabase` is great for learning and small projects, it may not be suitable for larger applications that require more robust database solutions.
