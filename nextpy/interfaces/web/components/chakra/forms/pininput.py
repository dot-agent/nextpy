# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""A pin input component."""
from __future__ import annotations

from typing import Any, Optional, Union

from nextpy.backend.vars import Var
from nextpy.constants import EventTriggers
from nextpy.interfaces.web.components.chakra import ChakraComponent, LiteralInputVariant
from nextpy.interfaces.web.components.component import Component
from nextpy.interfaces.web.components.tags.tag import Tag
from nextpy.interfaces.web.imports import ImportDict, merge_imports
from nextpy.utils import format


class PinInput(ChakraComponent):
    """The component that provides context to all the pin-input fields."""

    tag = "PinInput"

    # State var to bind the the input.
    value: Var[str]

    # If true, the pin input receives focus on mount
    auto_focus: Var[bool]

    # The default value of the pin input
    default_value: Var[str]

    # The border color when the input is invalid.
    error_border_color: Var[str]

    # The border color when the input is focused.
    focus_border_color: Var[str]

    # The top-level id string that will be applied to the input fields. The index of the input will be appended to this top-level id.
    id_: Var[str]

    # The length of the number input.
    length: Var[int]

    # If true, the pin input component is put in the disabled state
    is_disabled: Var[bool]

    # If true, the pin input component is put in the invalid state
    is_invalid: Var[bool]

    # If true, focus will move automatically to the next input once filled
    manage_focus: Var[bool]

    # If true, the input's value will be masked just like `type=password`
    mask: Var[bool]

    # The placeholder for the pin input
    placeholder: Var[str]

    # The type of values the pin-input should allow ("number" | "alphanumeric").
    type_: Var[str]

    # "outline" | "flushed" | "filled" | "unstyled"
    variant: Var[LiteralInputVariant]

    # The name of the form field
    name: Var[str]

    def _get_imports(self) -> ImportDict:
        """Include PinInputField explicitly because it may not be a child component at compile time.

        Returns:
            The merged import dict.
        """
        range_var = Var.range(0)
        return merge_imports(
            super()._get_imports(),
            PinInputField().get_imports(),  # type: ignore
            range_var._var_data.imports if range_var._var_data is not None else {},
        )

    def get_event_triggers(self) -> dict[str, Union[Var, Any]]:
        """Get the event triggers that pass the component's value to the handler.

        Returns:
            A dict mapping the event trigger to the var that is passed to the handler.
        """
        return {
            **super().get_event_triggers(),
            EventTriggers.ON_CHANGE: lambda e0: [e0],
            EventTriggers.ON_COMPLETE: lambda e0: [e0],
        }

    def get_ref(self) -> str | None:
        """Override ref handling to handle array refs.

        PinInputFields may be created dynamically, so it's not possible
        to compute their ref at compile time, so we return a cheating
        guess if the id is specified.

        The `ref` for this outer component will always be stripped off, so what
        is returned here only matters for form ref collection purposes.

        Returns:
            None.
        """
        if any(isinstance(c, PinInputField) for c in self.children):
            return None
        if self.id:
            return format.format_array_ref(self.id, idx=self.length)
        return super().get_ref()

    def _get_ref_hook(self) -> Optional[str]:
        """Override the base _get_ref_hook to handle array refs.

        Returns:
            The overrided hooks.
        """
        if self.id:
            ref = format.format_array_ref(self.id, None)
            refs_declaration = Var.range(self.length).foreach(
                lambda: Var.create_safe("useRef(null)", _var_is_string=False),
            )
            refs_declaration._var_is_local = True
            if ref:
                return (
                    f"const {ref} = {str(refs_declaration)}; "
                    f"{str(Var.create_safe(ref).as_ref())} = {ref}"
                )
            return super()._get_ref_hook()

    def _render(self) -> Tag:
        """Override the base _render to remove the fake get_ref.

        Returns:
            The rendered component.
        """
        return super()._render().remove_props("ref")

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Create a pin input component.

        If no children are passed in, the component will create a default pin input
        based on the length prop.

        Args:
            *children: The children of the component.
            **props: The props of the component.

        Returns:
            The pin input component.
        """
        if children:
            props.pop("length", None)
        elif "length" in props:
            field_props = {}
            if "id" in props:
                field_props["id"] = props["id"]
            if "name" in props:
                field_props["name"] = props["name"]
            children = [
                PinInputField.for_length(props["length"], **field_props),
            ]
        return super().create(*children, **props)


class PinInputField(ChakraComponent):
    """The text field that user types in - must be a direct child of PinInput."""

    tag = "PinInputField"

    # the position of the PinInputField inside the PinInput.
    # Default to None because it is assigned by PinInput when created.
    index: Optional[Var[int]] = None

    # The name of the form field
    name: Var[str]

    @classmethod
    def for_length(cls, length: Var | int, **props) -> Var:
        """Create a PinInputField for a PinInput with a given length.

        Args:
            length: The length of the PinInput.
            props: The props of each PinInputField (name will become indexed).

        Returns:
            The PinInputField.
        """
        name = props.get("name")

        def _create(i):
            if name is not None:
                props["name"] = f"{name}-{i}"
            return PinInputField.create(**props, index=i, key=i)

        return Var.range(length).foreach(_create)  # type: ignore

    def _get_ref_hook(self) -> Optional[str]:
        return None

    def get_ref(self):
        """Get the array ref for the pin input.

        Returns:
            The array ref.
        """
        if self.id:
            return format.format_array_ref(self.id, self.index)
