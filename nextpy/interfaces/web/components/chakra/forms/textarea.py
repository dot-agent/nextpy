# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""A textarea component."""
from __future__ import annotations

from typing import Any, Union

from nextpy.backend.vars import Var
from nextpy.constants import EventTriggers
from nextpy.interfaces.web.components.chakra import ChakraComponent, LiteralInputVariant
from nextpy.interfaces.web.components.component import Component
from nextpy.interfaces.web.components.core.debounce import DebounceInput


class TextArea(ChakraComponent):
    """A text area component."""

    tag = "Textarea"

    # State var to bind the input.
    value: Var[str]

    # The default value of the textarea.
    default_value: Var[str]

    # The placeholder text.
    placeholder: Var[str]

    # The border color when the input is invalid.
    error_border_color: Var[str]

    # The border color when the input is focused.
    focus_border_color: Var[str]

    # If true, the form control will be disabled.
    is_disabled: Var[bool]

    # If true, the form control will be invalid.
    is_invalid: Var[bool]

    # If true, the form control will be read-only.
    is_read_only: Var[bool]

    # If true, the form control will be required.
    is_required: Var[bool]

    # "outline" | "filled" | "flushed" | "unstyled"
    variant: Var[LiteralInputVariant]

    # The name of the form field
    name: Var[str]

    def get_event_triggers(self) -> dict[str, Union[Var, Any]]:
        """Get the event triggers that pass the component's value to the handler.

        Returns:
            A dict mapping the event trigger to the var that is passed to the handler.
        """
        return {
            **super().get_event_triggers(),
            EventTriggers.ON_CHANGE: lambda e0: [e0.target.value],
            EventTriggers.ON_FOCUS: lambda e0: [e0.target.value],
            EventTriggers.ON_BLUR: lambda e0: [e0.target.value],
            EventTriggers.ON_KEY_DOWN: lambda e0: [e0.key],
            EventTriggers.ON_KEY_UP: lambda e0: [e0.key],
        }

    @classmethod
    def create(cls, *children, **props) -> Component:
        """Create an Input component.

        Args:
            *children: The children of the component.
            **props: The properties of the component.

        Returns:
            The component.
        """
        if (
            isinstance(props.get("value"), Var) and props.get("on_change")
        ) or "debounce_timeout" in props:
            # Currently default to 50ms, which appears to be a good balance
            debounce_timeout = props.pop("debounce_timeout", 50)
            # create a debounced input if the user requests full control to avoid typing jank
            return DebounceInput.create(
                super().create(*children, **props), debounce_timeout=debounce_timeout
            )
        return super().create(*children, **props)
