"""Handle styling."""

from __future__ import annotations

from typing import Any

from nextpy import constants
from nextpy.backend.event import EventChain
from nextpy.frontend.imports import ReactImportVar
from nextpy.utils import format
from nextpy.backend.vars import BaseVar, Var, VarData

VarData.update_forward_refs()  # Ensure all type definitions are resolved

# Reference the global ColorModeContext
color_mode_var_data = VarData(  # type: ignore
    imports={
        f"/{constants.Dirs.CONTEXTS_PATH}": {ReactImportVar(tag="ColorModeContext")},
        "react": {ReactImportVar(tag="useContext")},
    },
    hooks={
        f"const [ {constants.ColorMode.NAME}, {constants.ColorMode.TOGGLE} ] = useContext(ColorModeContext)",
    },
)
# Var resolves to the current color mode for the app ("light" or "dark")
color_mode = BaseVar(
    _var_name=constants.ColorMode.NAME,
    _var_type="str",
    _var_data=color_mode_var_data,
)
# Var resolves to a function invocation that toggles the color mode
toggle_color_mode = BaseVar(
    _var_name=constants.ColorMode.TOGGLE,
    _var_type=EventChain,
    _var_data=color_mode_var_data,
)


def convert(style_dict):
    """Convert a style dictionary to a formatted style dictionary.

    This function formats the keys of the style dictionary to camel case,
    processes nested style dictionaries, and handles instances of the Var class.

    Args:
        style_dict (dict): A dictionary representing styles.

    Returns:
        tuple: A tuple containing the formatted style dictionary and VarData instance.
    """
    var_data = None  # Track import/hook data from any Vars in the style dict.
    out = {}
    for key, value in style_dict.items():
        key = format.to_camel_case(key)
        new_var_data = None
        if isinstance(value, dict):
            # Recursively format nested style dictionaries.
            out[key], new_var_data = convert(value)
        elif isinstance(value, Var):
            # If the value is a Var, extract the var_data and cast as str.
            new_var_data = value._var_data
            out[key] = str(value)
        else:
            # Otherwise, convert to Var to collapse VarData encoded in f-string.
            new_var = Var.create(value)
            if new_var is not None:
                new_var_data = new_var._var_data
            out[key] = value
        # Combine all the collected VarData instances.
        var_data = VarData.merge(var_data, new_var_data)
    return out, var_data


class Style(dict):
    """A dictionary-based class for managing styles.

    This class extends the standard Python dictionary to facilitate the handling
    of style attributes in a dynamic and structured manner.

    Attributes:
        _var_data (VarData): A VarData instance tracking import/hook data.
    """

    def __init__(self, style_dict: dict | None = None):
        """Initialize the style with a given dictionary.

        Args:
            style_dict (dict | None): A dictionary representing styles. Default is None.
        """
        style_dict, self._var_data = convert(style_dict or {})
        super().__init__(style_dict)

    def update(self, style_dict: dict | None, **kwargs):
        """Update the style with new attributes.

        This method allows updating the style dictionary with new attributes
        or overriding existing ones.

        Args:
            style_dict (dict | None): A dictionary representing new style attributes.
            kwargs: Additional key-value pairs to update the style dictionary with.
        """
        if kwargs:
            style_dict = {**(style_dict or {}), **kwargs}
        if not isinstance(style_dict, Style):
            converted_dict = type(self)(style_dict)
        else:
            converted_dict = style_dict
        # Combine our VarData with that of any Vars in the style_dict that was passed.
        self._var_data = VarData.merge(self._var_data, converted_dict._var_data)
        super().update(converted_dict)

    def __setitem__(self, key: str, value: Any):
        """Set an item in the style dictionary.

        Args:
            key (str): The key corresponding to the style attribute.
            value (Any): The value of the style attribute.
        """
        # Create a Var to collapse VarData encoded in f-string.
        _var = Var.create(value)
        if _var is not None:
            # Carry the imports/hooks when setting a Var as a value.
            self._var_data = VarData.merge(self._var_data, _var._var_data)
        super().__setitem__(key, value)
