import math
import os
from datetime import date, datetime, timedelta
from typing import Callable, List, Optional, Tuple, TypeVar, Union, cast

import ipyvue
import ipyvuetify
import reacton.core
import traitlets
from typing_extensions import Literal

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.alias import rv

T = TypeVar("T")


@widget.value_component(None)
def select_slider(
    label: str,
    value: Union[Tuple[int, int], widget.Reactive[Tuple[int, int]]] = (1, 3),
    min: int = 0,
    max: int = 10,
    step: int = 1,
    on_value: Callable[[Tuple[int, int]], None] = None,
    thumb_label: Union[bool, Literal["always"]] = True,
    tick_labels: Union[List[str], Literal["end_points"], bool] = False,
    disabled: bool = False,
    class_name : str = '',
    style: str = ''
) -> reacton.core.ValueElement[ipyvuetify.RangeSlider, Tuple[int, int]]:
    """Slider for controlling a range of integer values.

    ### Basic example:

    ```widget
    import nextpy.interfaces.jupyter

    int_range = widget.reactive((0, 42))


    @widget.component
    def Page():
        widget.SliderRangeInt("Some integer range", value=int_range, min=-10, max=120)
        widget.Markdown(f"**Int range value**: {int_range.value}")
        with widget.row():
            widget.button("Reset", on_click=lambda: int_range.set((0, 42)))
    ```

    ## Arguments
    * `label`: Label to display next to the slider.
    * `value`: The currently selected value.
    * `min`: Minimum value.
    * `max`: Maximum value.
    * `step`: Step size.
    * `on_value`: Callback to call when the value changes.
    * `thumb_label`: Show a thumb label when sliding (True), always ("always"), or never (False).
    * `tick_labels`: Show tick labels corresponding to the values (True),
            custom tick labels by passing a list of strings, only end_points ("end_points"),
            or no labels at all (False, the default).
    * `disabled`: Whether the slider is disabled.
    """
    reactive_value = widget.use_reactive(value, on_value)
    del value, on_value

    def set_value_cast(value):
        v1, v2 = value
        reactive_value.set((int(v1), int(v2)))

    updated_tick_labels = _produce_tick_labels(tick_labels, min, max, step)

    return cast(
        reacton.core.ValueElement[ipyvuetify.RangeSlider, Tuple[int, int]],
        rv.RangeSlider(
            v_model=reactive_value.value,
            on_v_model=set_value_cast,
            label=label,
            min=min,
            max=max,
            step=step,
            thumb_label=thumb_label,
            tick_labels=updated_tick_labels,
            dense=False,
            hide_details=True,
            disabled=disabled,
            class_=class_name,
            style_=style
        ),
    )

@widget.value_component(None)
def select_slider_float(
    label: str,
    value: Union[Tuple[float, float], widget.Reactive[Tuple[float, float]]] = (1.0, 3.0),
    min: float = 0.0,
    max: float = 10.0,
    step: float = 0.1,
    on_value: Callable[[Tuple[float, float]], None] = None,
    thumb_label: Union[bool, Literal["always"]] = True,
    tick_labels: Union[List[str], Literal["end_points"], bool] = False,
    disabled: bool = False,
    class_name : str = '',
    style: str = ''
) -> reacton.core.ValueElement[ipyvuetify.RangeSlider, Tuple[float, float]]:
    """Slider for controlling a range of float values.

    ### Basic example:

    ```widget
    import nextpy.interfaces.jupyter

    float_range = widget.reactive((0.1, 42.4))


    @widget.component
    def Page():
        widget.SliderRangeFloat("Some float range", value=float_range, min=-10, max=120)
        widget.Markdown(f"**Float range value**: {float_range.value}")
        with widget.row():
            widget.button("Reset", on_click=lambda: float_range.set((0.1, 42.4)))
    ```

    ## Arguments
    * `label`: Label to display next to the slider.
    * `value`: The current value.
    * `min`: The minimum value.
    * `max`: The maximum value.
    * `step`: The step size.
    * `on_value`: Callback to call when the value changes.
    * `thumb_label`: Show a thumb label when sliding (True), always ("always"), or never (False).
    * `tick_labels`: Show tick labels corresponding to the values (True),
            custom tick labels by passing a list of strings, only end_points ("end_points"),
            or no labels at all (False, the default).
    * `disabled`: Whether the slider is disabled.
    """
    reactive_value = widget.use_reactive(value, on_value)
    del value, on_value

    def set_value_cast(value):
        v1, v2 = value
        reactive_value.set((float(v1), float(v2)))

    updated_tick_labels = _produce_tick_labels(tick_labels, min, max, step)

    return cast(
        reacton.core.ValueElement[ipyvuetify.RangeSlider, Tuple[float, float]],
        rv.RangeSlider(
            v_model=reactive_value.value,
            on_v_model=set_value_cast,
            label=label,
            min=min,
            max=max,
            step=step,
            thumb_label=thumb_label,
            tick_labels=updated_tick_labels,
            dense=False,
            hide_details=True,
            disabled=disabled,
            class_=class_name,
            style_=style
        ),
    )


def _produce_tick_labels(tick_labels: Union[List[str], Literal["end_points"], bool], min: float, max: float, step: float) -> Optional[List[str]]:
    if tick_labels == "end_points":
        num_repeats = int(math.ceil((max - min) / step)) - 1
        _tick_labels = [str(min), *([""] * num_repeats), str(max)]
    elif tick_labels is False:
        _tick_labels = None
    elif tick_labels is True:
        _tick_labels, start = [], min

        while start < max:
            _tick_labels.append(str(start))
            start += step
        _tick_labels.append(str(max))
    else:
        _tick_labels = tick_labels

    return _tick_labels