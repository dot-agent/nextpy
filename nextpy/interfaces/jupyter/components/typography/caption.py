import reacton.ipyvuetify as v
from typing import List, Optional, Union
import nextpy.interfaces.jupyter as widget

@widget.component
def caption(
    label: Optional[str] = None,
    children=[],
    class_name: str = '',
    style: str = '',
    **kwargs
):
    caption_style = 'font-size: 0.8em; font-style: italic; color: gray; margin-top: 10px; '
    return v.Html(
        tag = 'h1',
        children=[*([label] if label is not None else []), *children],
        class_=class_name,
        style_=caption_style+style,
        **kwargs
    )