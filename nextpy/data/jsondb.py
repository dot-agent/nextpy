"""Use Json as DB"""

# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     username: str
#     email: str
#     password: str

# # Example Usage:
# db = JsonDatabase('users.json', model=User) # Json file to store the data

# new_user = User(username="johndoe", email="john@example.com", password="securepassword123")
# db.add(new_user) # Adds a new user to the JSON file
# users = db.query(username="johndoe") # Queries users by username
# print(users) # Output the list of users with username johndoe

# # Update a user by ID
# db.update(new_user.id, {"password": "newpassword123"})

import json
import os
import uuid
from filelock import FileLock
from typing import Type, TypeVar, List, Dict, Optional, Any
from sqlmodel import SQLModel, Field

T = TypeVar('T', bound=SQLModel)


class JsonDatabaseException(Exception):
    """Base class for all exceptions related to the JsonDatabase."""
    pass


class IdNotFoundError(JsonDatabaseException):
    """
    Raised when an ID cannot be found in the JsonDatabase.
    
    Attributes
    ----------
    id : int
        The ID that was not found.
    """
    def __init__(self, id: int) -> None:
        self.id = id
        super().__init__(f"ID {id} does not exist in the JSON database.")


class DataNotFoundError(JsonDatabaseException):
    """
    Raised when the specified data cannot be found in the JsonDatabase.

    Attributes
    ----------
    data : Dict[str, Any]
        The specific data that was not found.
    """
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data
        super().__init__(f"The data {data!r} does not exist in the JSON database.")


class SchemaError(JsonDatabaseException):
    """
    Raised when there is a schema inconsistency in JsonDatabase operations.

    Attributes
    ----------
    message : str
        Explanation of the schema error.
    """
    def __init__(self, message: str) -> None:
        super().__init__(message)


class JsonDatabase:
    """
    A class to implement a simple JSON-based database
    Most of the code is based on pysondb code

    ...

    Attributes
    ----------
    filename : str
        Name of the json file to be used.
    model : Type[T]
        SQLModel for data validation.
    id_fieldname : str, optional
        Field name for the ID.
    lock : filelock.FileLock
        File lock for handling concurrency issues.

    Methods
    -------
    add(instance: T) -> T
        Adds a data instance into the database.
    query(**kwargs) -> List[T]
        Query over the database with given parameters.
    get(id_value: int) -> Optional[T]
        Get an instance from the database by its id.
    delete(id_value: int) -> None
        Deletes an instance from the database by its id.
    update(id_value: int, new_data: Dict[str, Any]) -> None
        Updates an instance from the database by its id.
    """

    def __init__(self, filename: str, model: Type[T], id_fieldname: str = "id") -> None:
        """
        Constructs all the necessary attributes for the JsonDatabase object.

        Parameters
        ----------
        filename : str
            Name of the json file to be used.
        model: Type[T]
            SQLModel for data validation.
        id_fieldname: str, optional
            Field name for the ID.
        """
        self.filename = filename
        self.model = model
        self.id_fieldname = id_fieldname
        self.lock = FileLock(f"{filename}.lock")
        self._create_db()

    def _create_db(self) -> None:
        """
        Create a new json file if it does not exist.
        """
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as db_file:
                json.dump({"data": []}, db_file)

    def _get_id(self) -> int:
        """
        Generate a new id.

        Returns
        -------
        int
            A newly generated id.
        """
        return int(str(uuid.uuid4().int)[:18])

    def _read_data(self) -> Dict[str, Any]:
        """
        Read data from the json file.

        Returns
        -------
        Dict[str, Any]
            The data from the json file.
        """
        with self.lock, open(self.filename, "r") as db_file:
            return json.load(db_file)

    def _write_data(self, data: Dict[str, Any]) -> None:
        """
        Write the given data into the json file.

        Parameters
        ----------
        data: Dict[str, Any]
            Data to be written into the json file.
        """
        with self.lock, open(self.filename, "w") as db_file:
            json.dump(data, db_file, indent=2)

    def add(self, instance: T) -> T:
        """
        Adds a data instance into the database.

        Parameters
        ----------
        instance: T
            The instance to be added.

        Returns
        -------
        T
            The added instance.
        """
        data = self._read_data()
        if not isinstance(instance, self.model):
            raise ValueError(f"Instance must be of type {self.model.__name__}.")
        instance_data = instance.dict()
        if instance_data.get(self.id_fieldname) is None:
            instance_data[self.id_fieldname] = self._get_id()
        else:
            existing_ids = [d.get(self.id_fieldname) for d in data["data"]]
            if instance_data[self.id_fieldname] in existing_ids:
                raise ValueError(f"ID {instance_data[self.id_fieldname]} already exists.")
        data["data"].append(instance_data)
        self._write_data(data)
        instance.id = instance_data[self.id_fieldname]  # type: ignore
        return instance

    def query(self, **kwargs) -> List[T]:
        """
        Query over the database with given parameters.

        Parameters
        ----------
        kwargs: dict
            Field names and values for the query.

        Returns
        -------
        List[T]
            The instances that match the query.
        """
        data = self._read_data()["data"]
        if not kwargs:
            return [self.model(**record) for record in data]  # type: ignore

        filtered_data = [
            record for record in data if all(record.get(k) == v for k, v in kwargs.items())
        ]
        return [self.model(**record) for record in filtered_data]  # type: ignore

    def get(self, id_value: int) -> Optional[T]:
        """
        Get an instance from the database by its id.

        Parameters
        ----------
        id_value: int
            The id of the instance.

        Returns
        -------
        Optional[T]
            The instance if exists.
        """
        data = self._read_data()["data"]
        for record in data:
            if record[self.id_fieldname] == id_value:
                return self.model(**record)  # type: ignore
        raise IdNotFoundError(f"Id {id_value!r} does not exist.")

    def delete(self, id_value: int) -> None:
        """
        Deletes an instance from the database by its id.

        Parameters
        ----------
        id_value: int
            The id of the instance.
        """
        data = self._read_data()
        original_count = len(data["data"])
        data["data"] = [record for record in data["data"] if record[self.id_fieldname] != id_value]
        if len(data["data"]) == original_count:
            raise IdNotFoundError(f"Id {id_value} does not exist.")
        self._write_data(data)

    def update(self, id_value: int, new_data: Dict[str, Any]) -> None:
        """
        Updates an instance from the database by its id.

        Parameters
        ----------
        id_value: int
            The id of the instance.
        new_data: Dict[str, Any]
            New values for the instance fields.
        """
        data = self._read_data()
        item_updated = False
        for record in data["data"]:
            if record[self.id_fieldname] == id_value:
                record.update(new_data)
                item_updated = True
                break
        if not item_updated:
            raise IdNotFoundError(f"Id {id_value!r} not found.")
        self._write_data(data)

    def add_from_json(self, data: Dict[str, Any]) -> Any:
        """
        Adds an entry to the database from a JSON-style dictionary by automatically
        converting it to an SQLModel instance.

        Parameters
        ----------
        data : dict
            A dictionary representing the data to be added.

        Returns
        -------
        Any
            The ID of the added entry.
        """
        # Create an SQLModel instance using the dictionary.
        instance = self.model.parse_obj(data)

        # Add the instance to the database.
        added_instance = self.add(instance)

        # Return the ID of the added entry. Assuming the ID is set by the database.
        return getattr(added_instance, self.id_fieldname)