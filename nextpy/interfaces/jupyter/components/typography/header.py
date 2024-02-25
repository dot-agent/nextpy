import reacton.ipyvuetify as v
from typing import List, Optional, Union
import nextpy.interfaces.jupyter as widget

@widget.component
def header(
    label: Optional[str] = None,
    children=[],
    class_name: str = '',
    style: str = '',
    **kwargs
):
    return v.Html(
        tag = 'h1',
        children=[*([label] if label is not None else []), *children],
        class_=class_name,
        style_=style,
        **kwargs
    )