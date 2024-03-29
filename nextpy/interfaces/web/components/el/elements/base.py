# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Element classes. This is an auto-generated file. Do not edit. See ../generate.py."""
from typing import Union

from nextpy.backend.vars import Var as Var
from nextpy.interfaces.web.components.el.element import Element


class BaseHTML(Element):
    """Base class for common attributes."""

    #  Provides a hint for generating a keyboard shortcut for the current element.
    access_key: Var[Union[str, int, bool]]

    # Controls whether and how text input is automatically capitalized as it is entered/edited by the user.
    auto_capitalize: Var[Union[str, int, bool]]

    # Indicates whether the element's content is editable.
    content_editable: Var[Union[str, int, bool]]

    # Defines the ID of a <menu> element which will serve as the element's context menu.
    context_menu: Var[Union[str, int, bool]]

    # Defines the text direction. Allowed values are ltr (Left-To-Right) or rtl (Right-To-Left)
    dir: Var[Union[str, int, bool]]

    # Defines whether the element can be dragged.
    draggable: Var[Union[str, int, bool]]

    # Hints what media types the media element is able to play.
    enter_key_hint: Var[Union[str, int, bool]]

    # Defines whether the element is hidden.
    hidden: Var[Union[str, int, bool]]

    # Defines the type of the element.
    input_mode: Var[Union[str, int, bool]]

    # Defines the name of the element for metadata purposes.
    item_prop: Var[Union[str, int, bool]]

    # Defines the language used in the element.
    lang: Var[Union[str, int, bool]]

    # Defines the role of the element.
    role: Var[Union[str, int, bool]]

    # Assigns a slot in a shadow DOM shadow tree to an element.
    slot: Var[Union[str, int, bool]]

    # Defines whether the element may be checked for spelling errors.
    spell_check: Var[Union[str, int, bool]]

    # Defines the position of the current element in the tabbing order.
    tab_index: Var[Union[str, int, bool]]

    # Defines a tooltip for the element.
    title: Var[Union[str, int, bool]]

    # Specifies whether the content of an element should be translated or not.
    translate: Var[Union[str, int, bool]]
