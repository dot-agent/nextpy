# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Radix slider components."""

from typing import Any, Dict, Literal

from nextpy.backend.vars import Var
from nextpy.interfaces.web.components.component import Component
from nextpy.interfaces.web.components.radix.primitives.base import RadixPrimitiveComponent
from nextpy.interfaces.web.style import Style

LiteralSliderOrientation = Literal["horizontal", "vertical"]
LiteralSliderDir = Literal["ltr", "rtl"]


class SliderComponent(RadixPrimitiveComponent):
    """Base class for all @radix-ui/react-slider components."""

    library = "@radix-ui/react-slider@^1.1.2"


class SliderRoot(SliderComponent):
    """The Slider component comtaining all slider parts."""

    tag = "Root"
    alias = "RadixSliderRoot"

    default_value: Var[list[int]]

    value: Var[list[int]]

    name: Var[str]

    disabled: Var[bool]

    orientation: Var[LiteralSliderOrientation]

    dir: Var[LiteralSliderDir]

    inverted: Var[bool]

    min: Var[int]

    max: Var[int]

    step: Var[int]

    min_steps_between_thumbs: Var[int]

    def get_event_triggers(self) -> Dict[str, Any]:
        """Event triggers for radix slider primitive.

        Returns:
            The triggers for event supported by radix primitives.
        """
        return {
            **super().get_event_triggers(),
            "on_value_change": lambda e0: [e0],  # trigger for all change of a thumb
            "on_value_commit": lambda e0: [e0],  # trigger when thumb is released
        }

    def _apply_theme(self, theme: Component):
        self.style = Style(
            {
                "position": "relative",
                "display": "flex",
                "align_items": "center",
                "user_select": "none",
                "touch_action": "none",
                "width": "200px",
                "height": "20px",
                "&[data-orientation='vertical']": {
                    "flex_direction": "column",
                    "width": "20px",
                    "height": "100px",
                },
                **self.style,
            }
        )


class SliderTrack(SliderComponent):
    """A Slider Track component."""

    tag = "Track"
    alias = "RadixSliderTrack"

    def _apply_theme(self, theme: Component):
        self.style = Style(
            {
                "position": "relative",
                "flex_grow": "1",
                "background_color": "black",
                "border_radius": "9999px",
                "height": "3px",
                "&[data-orientation='vertical']": {
                    "width": "3px",
                },
                **self.style,
            }
        )


class SliderRange(SliderComponent):
    """A SliderRange component."""

    tag = "Range"
    alias = "RadixSliderRange"

    def _apply_theme(self, theme: Component):
        self.style = Style(
            {
                "position": "absolute",
                "background_color": "white",
                "height": "100%",
                "&[data-orientation='vertical']": {
                    "width": "100%",
                },
                **self.style,
            }
        )


class SliderThumb(SliderComponent):
    """A SliderThumb component."""

    tag = "Thumb"
    alias = "RadixSliderThumb"

    def _apply_theme(self, theme: Component):
        self.style = Style(
            {
                "display": "block",
                "width": "20px",
                "height": "20px",
                "background_color": "black",
                "box_shadow": "0 2px 10px black",
                "border_radius": "10px",
                "&:hover": {
                    "background_color": "gray",
                },
                "&:focus": {
                    "outline": "none",
                    "box_shadow": "0 0 0 4px gray",
                },
                **self.style,
            }
        )


slider_root = SliderRoot.create
slider_track = SliderTrack.create
slider_range = SliderRange.create
slider_thumb = SliderThumb.create


def slider(
    **props,
) -> Component:
    """High level API for slider.

    Args:
        **props: The props of the slider.

    Returns:
        A slider component.
    """
    track = SliderTrack.create(SliderRange.create())
    # if default_value is not set, the thumbs will not render properly but the slider will still work
    if "default_value" in props:
        children = [
            track,
            *[SliderThumb.create() for _ in props.get("default_value", [])],
        ]
    else:
        children = [
            track,
            #     Foreach.create(props.get("value"), lambda e: SliderThumb.create()),  # foreach doesn't render Thumbs properly
        ]

    return slider_root(*children, **props)
