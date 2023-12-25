"""Implements the Singleton design pattern to ensure only one instance of a class
is created. Provides a get_instance() method to retrieve the singleton instance
and initialize() to create the instance if it does not already exist.

Example usage:

from singleton import Singleton

class MyClass(Singleton):
    pass

obj1 = MyClass.get_instance() 
obj2 = MyClass.get_instance()

assert obj1 is obj2
"""
class Singleton:
    """Singleton design pattern implementation."""

    _instances = {}

    @classmethod
    def get_instance(cls, *args, **kwargs):
        """Static access method to get the singleton instance.

        Args:
            *args: Positional arguments to pass to the constructor.
            **kwargs: Keyword arguments to pass to the constructor.


        Returns:
            The singleton instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = cls(*args, **kwargs)
        return cls._instances[cls]

    @classmethod
    def initialize(cls, *args, **kwargs):
        """Static access method to initialize the singleton instance.


        Args:
            *args: Positional arguments to pass to the constructor.
            **kwargs: Keyword arguments to pass to the constructor.
        """
        if cls not in cls._instances:
            cls._instances[cls] = cls(*args, **kwargs)
