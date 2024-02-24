import reacton.ipyvuetify as v
from typing import List, Optional, Union
import nextpy.interfaces.jupyter as widget

# from nextpy.interfaces.jupyter.util import _combine_classes

@widget.component
def text(
    label: Optional[str] = None,
    children: List = [],
    class_name: str = '',
    style:str = '',
    **kwargs,
):
    return v.Text(
        children=[*([label] if label is not None else []), *children],
        class_=class_name,
        style_=style,
        **kwargs,
    )