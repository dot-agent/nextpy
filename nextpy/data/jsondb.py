"""Use Json as DB."""
import json
import os
import uuid
from typing import Any, Dict, List, Optional, Type, TypeVar

from filelock import FileLock
from sqlmodel import SQLModel

T = TypeVar("T", bound=SQLModel)


class JsonDatabaseException(Exception):
    """Base class for exceptions in the JsonDatabase.

    This class serves as a base for all exceptions related to operations
    in the JsonDatabase, ensuring a unified interface for exception handling.
    """

    pass


class IdNotFoundError(JsonDatabaseException):
    """Exception raised when an ID is not found in the JsonDatabase.

    Attributes:
        id (int): The ID that was not found in the database.

    Args:
        id (int): The ID that could not be found.

    Raises:
        IdNotFoundError: If the specified ID does not exist in the database.
    """

    def __init__(self, id: int) -> None:
        """Raises error if ID does not exist ."""
        self.id = id
        super().__init__(f"ID {id} does not exist in the JSON database.")


class DataNotFoundError(JsonDatabaseException):
    """Exception raised when specific data is not found in the JsonDatabase.

    Attributes:
        data (Dict[str, Any]): The data that was not found in the database.

    Args:
        data (Dict[str, Any]): The specific data that could not be found.

    Raises:
        DataNotFoundError: If the specified data does not exist in the database.
    """

    def __init__(self, data: Dict[str, Any]) -> None:
        """Raises error if the specified data does not."""
        self.data = data
        super().__init__(f"The data {data!r} does not exist in the JSON database.")


class SchemaError(JsonDatabaseException):
    """Exception raised for schema inconsistencies in JsonDatabase operations.

    Attributes:
        message (str): The error message detailing the schema inconsistency.

    Args:
        message (str): Explanation of the schema error encountered.

    Raises:
        SchemaError: If there is a schema-related issue during database operations.
    """

    def __init__(self, message: str) -> None:
        """Raises error for schema inconsistencies."""
        super().__init__(message)


class JsonDatabase:
    """A simple JSON-based database for CRUD operations.

    This class supports basic CRUD (Create, Read, Update, Delete) operations
    on a JSON file, utilizing SQLModel for data validation and schema definition.

    Attributes:
        filename (str): Name of the json file to be used.
        model (Type[T]): SQLModel for data validation.
        id_fieldname (str): Field name for the ID, optional.
        lock (filelock.FileLock): File lock for handling concurrency issues.

    Methods:
        add(instance: T) -> T
            Adds a data instance into the database.
        query(**kwargs) -> List[T]
            Query over the database with given parameters.
        get(id_value: int) -> Optional[T]
            Get an instance from the database by its id.
        delete(id_value: int) -> None
            Deletes an instance from the database by its id.
        update(id_value: int, new_data: Dict[str, Any]) -> None
            Updates an instance in the database by its id.

    Example Usage:
        # Define a User model using SQLModel
        class User(SQLModel, table=True):
            id: Optional[int] = Field(default=None, primary_key=True)
            username: str
            email: str
            password: str

        # Initialize the JSON database with the User model
        db = JsonDatabase('users.json', model=User)

        # Create a new user and add to the database
        new_user = User(username="johndoe", email="john@example.com", password="securepassword123")
        db.add(new_user)

        # Query users by username
        users = db.query(username="johndoe")
        print(users)  # Outputs the list of users with username 'johndoe'

        # Update a user's password by ID
        db.update(new_user.id, {"password": "newpassword123"})
    """

    def __init__(self, filename: str, model: Type[T], id_fieldname: str = "id") -> None:
        """Initializes the JsonDatabase object.

        Args:
            filename (str): The JSON file name for the database.
            model (Type[T]): The SQLModel class for data validation.
            id_fieldname (str): The ID field name (defaults to "id").
        """
        self.filename = filename
        self.model = model
        self.id_fieldname = id_fieldname
        self.lock = FileLock(f"{filename}.lock")
        self._create_db()

    def _create_db(self) -> None:
        """Creates a new JSON file for the database if it does not already exist."""
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as db_file:
                json.dump({"data": []}, db_file)

    def _get_id(self) -> int:
        """Generates a new unique ID.

        Returns:
            int: A newly generated unique ID.
        """
        return int(str(uuid.uuid4().int)[:18])

    def _read_data(self) -> Dict[str, Any]:
        """Reads data from the JSON file.

        Returns:
            Dict[str, Any]: The data stored in the JSON file.
        """
        with self.lock, open(self.filename, "r") as db_file:
            return json.load(db_file)

    def _write_data(self, data: Dict[str, Any]) -> None:
        """Writes the given data into the JSON file.

        Args:
            data (Dict[str, Any]): Data to be written into the JSON file.
        """
        with self.lock, open(self.filename, "w") as db_file:
            json.dump(data, db_file, indent=2)

    def add(self, instance: T) -> T:
        """Adds a new data instance into the database.

        Args:
            instance (T): The data instance to be added.

        Returns:
            T: The added data instance, with ID assigned.

        Raises:
            ValueError: If the instance is not of the correct model type or if the ID already exists.
        """
        data = self._read_data()
        if not isinstance(instance, self.model):
            raise ValueError(f"Instance must be of type {self.model.__name__}.")
        instance_data = instance.model_dump()
        if instance_data.get(self.id_fieldname) is None:
            instance_data[self.id_fieldname] = self._get_id()
        else:
            existing_ids = [d.get(self.id_fieldname) for d in data["data"]]
            if instance_data[self.id_fieldname] in existing_ids:
                raise ValueError(
                    f"ID {instance_data[self.id_fieldname]} already exists."
                )
        data["data"].append(instance_data)
        self._write_data(data)
        instance.id = instance_data[self.id_fieldname]  # type: ignore
        return instance

    def query(self, **kwargs) -> List[T]:
        """Queries the database with the given parameters.

        Args:
            **kwargs: Field names and values for the query.

        Returns:
            List[T]: A list of instances that match the query.
        """
        data = self._read_data()["data"]
        if not kwargs:
            return [self.model(**record) for record in data]  # type: ignore

        filtered_data = [
            record
            for record in data
            if all(record.get(k) == v for k, v in kwargs.items())
        ]
        return [self.model(**record) for record in filtered_data]  # type: ignore

    def get(self, id_value: int) -> Optional[T]:
        """Retrieves an instance from the database by its ID.

        Args:
            id_value (int): The ID of the instance to retrieve.

        Returns:
            Optional[T]: The retrieved instance, or None if not found.

        Raises:
            TypeError: If id_value is not an integer.
            IdNotFoundError: If no instance with the given ID is found.
        """
        if not isinstance(id_value, int):
            raise TypeError(
                f"Expected id_value to be an int, got {type(id_value).__name__} instead."
            )

        data = self._read_data()["data"]
        for record in data:
            if record.get(self.id_fieldname) == id_value:
                return self.model(**record)  # type: ignore

        raise IdNotFoundError(f"Id {id_value!r} does not exist.")

    def delete(self, id_value: int) -> None:
        """Deletes an instance from the database by its ID.

        Args:
            id_value (int): The ID of the instance to delete.

        Raises:
            TypeError: If id_value is not an integer.
            IdNotFoundError: If no instance with the given ID is found.
        """
        if not isinstance(id_value, int):
            raise TypeError(
                f"Expected id_value to be an int, got {type(id_value).__name__} instead."
            )

        data = self._read_data()
        original_count = len(data["data"])
        data["data"] = [
            record
            for record in data["data"]
            if record.get(self.id_fieldname) != id_value
        ]
        if len(data["data"]) == original_count:
            raise IdNotFoundError(f"Id {id_value} does not exist.")
        self._write_data(data)

    def update(self, id_value: int, new_data: Dict[str, Any]) -> None:
        """Updates an instance in the database by its ID.

        Args:
            id_value (int): The ID of the instance to update.
            new_data (Dict[str, Any]): New values for the instance fields.

        Raises:
            TypeError: If id_value is not an integer.
            IdNotFoundError: If no instance with the given ID is found.
        """
        if not isinstance(id_value, int):
            raise TypeError(
                f"Expected id_value to be an int, got {type(id_value).__name__} instead."
            )

        data = self._read_data()
        item_updated = False
        for record in data["data"]:
            if record.get(self.id_fieldname) == id_value:
                record.update(new_data)
                item_updated = True
                break
        if not item_updated:
            raise IdNotFoundError(f"Id {id_value!r} not found.")
        self._write_data(data)

    def add_from_json(self, data: Dict[str, Any]) -> Any:
        """Adds an entry to the database from a JSON-style dictionary.

        Args:
            data (Dict[str, Any]): A dictionary representing the data to be added.

        Returns:
            Any: The ID of the added entry.

        Raises:
            ValueError: If the 'id' field is not convertible to an integer.
        """
        # Check if 'id' is in data and convert it to an integer if necessary
        if self.id_fieldname in data:
            try:
                data[self.id_fieldname] = int(data[self.id_fieldname])
            except ValueError as err:  # Capture the original ValueError in `err`  
                # Now raise a new ValueError with `from err` to chain the exceptions  
               raise ValueError(f"The '{self.id_fieldname}' field must be convertible to an integer.") from err

        # Create an SQLModel instance using the dictionary.
        instance = self.model.model_validate(data)

        # Add the instance to the database.
        added_instance = self.add(instance)

        # Return the ID of the added entry. Assuming the ID is set by the database.
        return getattr(added_instance, self.id_fieldname)
