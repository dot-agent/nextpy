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


@widget.value_component(int)
def slider(
    label: str,
    value: Union[int, widget.Reactive[int]] = 0,
    min: int = 0,
    max: int = 10,
    step: int = 1,
    on_value: Optional[Callable[[int], None]] = None,
    thumb_label: Union[bool, Literal["always"]] = True,
    tick_labels: Union[List[str], Literal["end_points"], bool] = False,
    disabled: bool = False,
    class_name : str = '',
    style: str = ''
):
    """Slider for controlling an integer value.

    ### Basic example:

    ```widget
    import nextpy.interfaces.jupyter

    int_value = widget.reactive(42)


    @widget.component
    def Page():
        widget.SliderInt("Some integer", value=int_value, min=-10, max=120)
        widget.Markdown(f"**Int value**: {int_value.value}")
        with widget.row():
            widget.button("Reset", on_click=lambda: int_value.set(42))
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
        reactive_value.value = int(value)

    updated_tick_labels = _produce_tick_labels(tick_labels, min, max, step)

    return rv.Slider(
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
    )


@widget.value_component(float)
def slider_float(
    label: str,
    value: Union[float, widget.Reactive[float]] = 0,
    min: float = 0,
    max: float = 10.0,
    step: float = 0.1,
    on_value: Callable[[float], None] = None,
    thumb_label: Union[bool, Literal["always"]] = True,
    tick_labels: Union[List[str], Literal["end_points"], bool] = False,
    disabled: bool = False,
    class_name : str = '',
    style: str = ''
):
    """Slider for controlling a float value.

    ### Basic example:

    ```widget
    import nextpy.interfaces.jupyter

    float_value = widget.reactive(42.4)


    @widget.component
    def Page():
        widget.SliderFloat("Some integer", value=float_value, min=-10, max=120)
        widget.Markdown(f"**Float value**: {float_value.value}")
        with widget.row():
            widget.button("Reset", on_click=lambda: float_value.set(42.5))
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
        reactive_value.set(float(value))

    updated_tick_labels = _produce_tick_labels(tick_labels, min, max, step)

    return rv.Slider(
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
    )


@widget.value_component(None)
def slider_value(
    label: str,
    value: Union[T, widget.Reactive[T]],
    values: List[T],
    on_value: Callable[[T], None] = None,
    disabled: bool = False,
    class_name : str = '',
    style: str = ''
) -> reacton.core.ValueElement[ipyvuetify.Slider, T]:
    """Slider for selecting a value from a list of values.

    ### Basic example:

    ```widget
    import nextpy.interfaces.jupyter

    foods = ["Kiwi", "Banana", "Apple"]
    food = widget.reactive("Banana")


    @widget.component
    def Page():
        widget.SliderValue(label="Food", value=food, values=foods)
        widget.Markdown(f"**Selected**: {food.value}")
    ```

    ## Arguments
    * `label`: Label to display next to the slider.
    * `value`: The currently selected value.
    * `values`: List of values to select from.
    * `on_value`: Callback to call when the value changes.
    * `disabled`: Whether the slider is disabled.

    """
    reactive_value = widget.use_reactive(value, on_value)
    del value, on_value
    index, set_index = widget.use_state(values.index(reactive_value.value), key="index")

    def on_index(index):
        set_index(index)
        value = values[index]
        reactive_value.set(value)

    return cast(
        reacton.core.ValueElement[ipyvuetify.Slider, T],
        rv.Slider(
            v_model=index,
            on_v_model=on_index,
            ticks=True,
            tick_labels=values,
            label=label,
            min=0,
            max=len(values) - 1,
            dense=False,
            hide_details=True,
            disabled=disabled,
            class_=class_name,
            style_=style 
        ),
    )


class DateSliderWidget(ipyvue.VueTemplate):
    template_file = os.path.realpath(os.path.join(os.path.dirname(__file__), "slider_date.vue"))

    min = traitlets.CFloat(0).tag(sync=True)
    days = traitlets.CFloat(0).tag(sync=True)
    value = traitlets.Any(0).tag(sync=True)

    label = traitlets.Unicode("").tag(sync=True)
    disabled = traitlets.Bool(False).tag(sync=True)


@widget.value_component(date)
def slider_date(
    label: str,
    value: Union[date, widget.Reactive[date]] = date(2010, 7, 28),
    min: date = date(1981, 1, 1),
    max: date = date(2050, 12, 30),
    on_value: Callable[[date], None] = None,
    disabled: bool = False,
    class_name : str = '',
    style: str = ''
):
    """Slider for controlling a date value.

    ### Basic example:

    ```widget
    import nextpy.interfaces.jupyter
    import datetime

    date_value = widget.reactive(datetime.date(2010, 7, 28))


    @widget.component
    def Page():
        widget.SliderDate("Some date", value=date_value)
        widget.Markdown(f"**Date value**: {date_value.value.strftime('%Y-%b-%d')}")
        with widget.row():
            widget.button("Reset", on_click=lambda: date_value.set(datetime.date(2010, 7, 28)))
    ```

    ## Arguments
    * `label`: Label to display next to the slider.
    * `value`: The current value.
    * `min`: The minimum value.
    * `max`: The maximum value.
    * `on_value`: Callback to call when the value changes.
    * `disabled`: Whether the slider is disabled.
    """
    reactive_value = widget.use_reactive(value, on_value)
    del value, on_value

    def format(d: date):
        return float(datetime(d.year, d.month, d.day).timestamp())

    dt_min = format(min)
    delta: timedelta = max - min
    days = delta.days

    delta_value: timedelta = reactive_value.value - min
    days_value = delta_value.days
    if days_value < 0:
        days_value = 0

    def set_value_cast(value):
        date = min + timedelta(days=value)
        reactive_value.set(date)

    return DateSliderWidget.element(label=label, min=dt_min, days=days, on_value=set_value_cast, value=days_value, 
                                    disabled=disabled, class_=class_name, style_=style)


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


# FloatSlider = SliderFloat
# IntSlider = SliderInt
# ValueSlider = SliderValue
# DateSlider = SliderDate
