"""Handles React Component Imports.

Provides classes and functions to manage React component imports in Python code,
facilitating the rendering process into React.

Classes
-------
ReactComponentName : Base
    Represents an import declaration for React components. This class includes 
    various properties to accurately describe how the component should be imported,
    such as whether it is a default import, the tag name of the import, potential
    alias, and if it is necessary to install the associated library or include 
    the import in the rendering output. It addresses challenges related to default 
    imports with names differing from their originating libraries.

Functions
---------
merge_imports(*imports)
    Combines several import dictionaries into a single one, streamlining the handling
    of React component imports across multiple parts of a codebase. This function is
    especially useful when constructing a cumulative list of imports from disparate 
    components or files.

Examples
--------
>>> TODO
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, List, Optional

from nextpy.base import Base


def merge_imports(*imports) -> ImportDict:
    """Merge multiple dictionaries of imports into a single dictionary.

    Each key in the dictionary is a library name and the corresponding value
    is a list of ReactComponentName objects representing imports from that library.

    Parameters
    ----------
    *imports : ImportDict
        Variable number of import dictionaries to merge.

    Returns
    -------
    ImportDict
        A single dictionary containing all merged imports.
    """
    all_imports = defaultdict(list)
    for import_dict in imports:
        for lib, fields in import_dict.items():
            all_imports[lib].extend(fields)
    return all_imports


def collapse_imports(imports: ImportDict) -> ImportDict:
    """Remove all duplicate ReactImportVar within an ImportDict.

    Args:
        imports: The import dict to collapse.

    Returns:
        The collapsed import dict.
    """
    return {lib: list(set(import_vars)) for lib, import_vars in imports.items()}


class ReactImportVar(Base):
    """Class representing an import variable for a React component.

    This class enables explicit definition of the import statement,
    such as whether it should be treated as a default import and whether an alias should
    be used. This is particularly useful when the name of the imported component (tag name)
    differs from the name of the library or when a specific naming convention is required.

    Attributes
    ----------
    tag : Optional[str]
        The name of the import tag (module or variable name).

    is_default : Optional[bool]
        Flag indicating whether the import is a default import or named. Defaults to False.

    alias : Optional[str]
        The alias of the tag. Defaults to None.

    install : Optional[bool]
        Flag indicating whether the associated library should be installed. Defaults to True.

    render : Optional[bool]
        Flag indicating whether this import should be rendered or not. Defaults to True.

    Methods
    -------
    name()
        Retrieves the full name of the import, including alias if present.

    __hash__()
        Returns a hash value for the ReactComponentName instance.
    """

    # The name of the import tag.
    tag: Optional[str]

    # whether the import is default or named.
    is_default: Optional[bool] = False

    # The tag alias.
    alias: Optional[str] = None

    # Whether this import need to install the associated lib
    install: Optional[bool] = True

    # whether this import should be rendered or not
    render: Optional[bool] = True

    @property
    def name(self) -> str:
        """Returns the alias of the object if it exists and is the default,
        else returns the tag and alias joined with ' as '.
        If neither exists, it will return an empty string.

        Returns
        -------
        str
            The display name of the import.
        """
        if self.alias:
            return self.alias if self.is_default else " as ".join([self.tag, self.alias])  # type: ignore
        else:
            return self.tag or ""

    def __hash__(self) -> int:
        """Generates a hash value for this ReactComponentName instance.

        Returns
        -------
        int
            The hash value for the instance, based on its attributes.
        """
        return hash((self.tag, self.is_default, self.alias, self.install, self.render))


ImportDict = Dict[str, List[ReactImportVar]]
