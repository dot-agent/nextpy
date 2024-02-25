import reacton.ipyvuetify as v
from typing import List, Optional, Union
import nextpy.interfaces.jupyter as widget
import datetime

@widget.component
def time_picker(
    label: Optional[str] = None,
    value: Optional[Union[datetime.time, str]] = "now",
    class_name: str = '',
    style: str = '',
    **kwargs,
):
    if isinstance(value, datetime.time):
        value = value.strftime('%H:%M')

    if value == "now":
        value = datetime.datetime.now().strftime('%H:%M')

    return v.TimePicker(
        label=label,
        v_model=value,
        class_=class_name,
        style_=style,
        **kwargs,
    )
