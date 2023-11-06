"""Data Ops utility functions."""
import os
from typing import Any, Dict, Optional,List



def get_from_dict_or_env(data: Optional[Dict[str, Any]] = None, key: Optional[str] = None, env_key: Optional[str] = None, default: Optional[str] = None) -> str:
    """Get a value from a dictionary or an environment variable."""
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
    if isinstance(val, str):
        return val
    elif isinstance(val, dict):
        return "\n" + stringify_dict(val)
    elif isinstance(val, list):
        return "\n".join(stringify_value(v) for v in val)
    else:
        return str(val)


def stringify_dict(data: dict) -> str:
    text = ""
    for key, value in data.items():
        text += key + ": " + stringify_value(value) + "\n"
    return text

def comma_list(items: List[Any]) -> str:
    return ", ".join(str(item) for item in items)

