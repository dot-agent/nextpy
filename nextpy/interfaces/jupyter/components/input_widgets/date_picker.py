import reacton.ipyvuetify as v
import typing
from typing import List, Optional, Union
import nextpy.interfaces.jupyter as widget

@widget.component
def date_picker(
    label: Optional[str] = None,
    children: List = [],
    class_name: str = '',
    style: str = '',
    min: str = None,
    max: str = None,
    value: typing.Union[list, str] = None,  
    **kwargs,
):
    
    effective_value = value if value is not None else ""  

    return v.DatePicker(
        children=[*([label] if label is not None else []), *children],
        class_=class_name,
        style_=style,
        min=min,
        max=max,
        value=effective_value,  
        **kwargs,
    )