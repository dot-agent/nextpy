import reacton.ipyvuetify as v
from typing import List, Optional, Union
import nextpy.interfaces.jupyter as widget

@widget.component
def divider(
    children=[],
    class_name: str = '',
    style:str = '',
    vertical: bool = None,
    **kwargs,
):
    return v.Divider(
        children=[*children],
        class_=class_name,
        style_=style,
        vertical=vertical,
        **kwargs,
    )