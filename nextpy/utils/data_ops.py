"""Data Ops utility functions."""

import os
from typing import Any, Dict, List, Optional


def get_from_dict_or_env(
    data: Optional[Dict[str, Any]] = None,
    key: Optional[str] = None,
    env_key: Optional[str] = None,
    default: Optional[str] = None,
) -> str:
    """Retrieve a value from a given dictionary or environment variable.
    
    Args:
        data (Optional[Dict[str, Any]]): The dictionary to look for the key. Defaults to None.
        key (Optional[str]): The key to search in the dictionary. Defaults to None.
        env_key (Optional[str]): The environment variable to check if key is not found in dictionary. Defaults to None.
        default (Optional[str]): The default value to return if key is not found in both dictionary and environment variables. Defaults to None.

    Returns:
        str: The value corresponding to the key from the dictionary or environment variable.

    Raises:
        ValueError: If the key is not found in both the dictionary and environment variables, and no default is provided.
    """
    if key and data and key in data and data[key]:
        return data[key]
    elif env_key and env_key in os.environ and os.environ[env_key]:
        return os.environ[env_key]
    elif default is not None:
        return default
    else:
        raise ValueError(
            f"Did not find {key or env_key}, please add an environment variable"
            f" `{env_key}` which contains it, or pass"
            f"  `{key}` as a named parameter."
        )


def stringify_value(val: Any) -> str:
    """Convert a given value into a string.

    Args:
        val (Any): The value to be converted into a string.

    Returns:
        str: The string representation of the value.
    """
    if isinstance(val, str):
        return val
    elif isinstance(val, dict):
        return "\n" + stringify_dict(val)
    elif isinstance(val, list):
        return "\n".join(stringify_value(v) for v in val)
    else:
        return str(val)


def stringify_dict(data: dict) -> str:
    """Convert a dictionary into a string.

    Args:
        data (dict): The dictionary to be converted into a string.

    Returns:
        str: The string representation of the dictionary with each key-value pair on a new line.
    """
    text = ""
    for key, value in data.items():
        text += key + ": " + stringify_value(value) + "\n"
    return text


def comma_list(items: List[Any]) -> str:
    """Convert a list into a string, with items separated by commas.

    Args:
        items (List[Any]): The list to be converted into a string.

    Returns:
        str: The string representation of the list, with items separated by commas.
    """
    return ", ".join(str(item) for item in items)
