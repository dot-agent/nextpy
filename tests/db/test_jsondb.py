# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import pytest
from sqlmodel import Field, SQLModel

from nextpy.data.jsondb import IdNotFoundError, JsonDatabase


# Create a mock SQLModel class for testing purposes
class MockUser(SQLModel, table=True):
    """A data model representing a user in a SQL database.

    Args:
        id (int): The primary key for the user table.
        username (str): The username of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
    """

    id: int = Field(default=None, primary_key=True)
    username: str
    email: str
    password: str

# Set up a fixture for the test database with our MockUser class
@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test_users.json"
    db = JsonDatabase(str(db_path), model=MockUser)
    return db

# Test adding a new user
def test_add_new_user(test_db):
    new_user = MockUser(username="johndoe", email="john@example.com", password="securepassword123")
    added_user = test_db.add(new_user)
    assert added_user.id is not None

# Test adding a user with pre-existing ID
def test_add_user_with_existing_id(test_db):
    new_user = MockUser(username="janedoe", email="jane@example.com", password="securepassword456")
    added_user = test_db.add(new_user)
    with pytest.raises(ValueError):
        test_db.add(MockUser(id=added_user.id, username="janeduplicate", email="jane@example.com", password="securepassword456"))


# Test adding a new user with a JSON object
def test_add_user_from_json(test_db):
    user_data = {
        "username": "jsonuser",
        "email": "jsonuser@example.com",
        "password": "mysecurepassword"
    }
    user_id = test_db.add_from_json(user_data)
    assert user_id is not None
    added_user = test_db.get(user_id)
    assert added_user.username == user_data['username']
    assert added_user.email == user_data['email']
    assert added_user.password == user_data['password']


# Test querying users
def test_query_users(test_db):
    new_user_john = MockUser(username="johndoe", email="john@example.com", password="securepassword123")
    test_db.add(new_user_john)

    new_user_jane = MockUser(username="janedoe", email="jane@example.com", password="securepassword456")
    test_db.add(new_user_jane)

    results = test_db.query(username="johndoe")
    assert len(results) == 1
    assert results[0].username == "johndoe"

# Test getting a user by ID
def test_get_user_by_id(test_db):
    new_user = MockUser(username="johndoe", email="john@example.com", password="securepassword123")
    added_user = test_db.add(new_user)

    retrieved_user = test_db.get(added_user.id)
    assert retrieved_user.id == added_user.id

# Test getting a non-existent user
def test_get_nonexistent_user_by_id(test_db):
    with pytest.raises(IdNotFoundError):
        test_db.get(999)

# Test updating a user
def test_update_user_by_id(test_db):
    new_user = MockUser(username="johndoe", email="john@example.com", password="securepassword123")
    added_user = test_db.add(new_user)

    test_db.update(added_user.id, {"password": "newpassword123"})
    updated_user = test_db.get(added_user.id)
    assert updated_user.password == "newpassword123"

# Test updating a non-existent user
def test_update_nonexistent_user_by_id(test_db):
    with pytest.raises(IdNotFoundError):
        test_db.update(999, {"password": "newpassword123"})

# Test deleting a user
def test_delete_user_by_id(test_db):
    new_user = MockUser(username="johndoe", email="john@example.com", password="securepassword123")
    added_user = test_db.add(new_user)

    test_db.delete(added_user.id)
    with pytest.raises(IdNotFoundError):
        test_db.get(added_user.id)

# Test deleting a non-existent user
def test_delete_nonexistent_user_by_id(test_db):
    with pytest.raises(IdNotFoundError):
        test_db.delete(999)

# Run the tests, if this file is invoked directly
if __name__ == "__main__":
    pytest.main(["-s"])
