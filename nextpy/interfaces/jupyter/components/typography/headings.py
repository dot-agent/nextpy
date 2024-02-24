import reacton.ipyvuetify as v
from typing import List, Optional, Union
import nextpy.interfaces.jupyter as widget

from nextpy.interfaces.jupyter.util import _combine_classes

@widget.component
def h1(
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

@widget.component
def h2(
    label: Optional[str] = None,
    children=[],
    class_name: str = '',
    style: str = '',
    **kwargs
):
    return v.Html(
        tag = 'h2',
        children=[*([label] if label is not None else []), *children],
        class_=class_name,
        style_=style,
        **kwargs
    )

@widget.component
def h3(
    label: Optional[str] = None,
    children=[],
    class_name: str = '',
    style: str = '',
    **kwargs
):
    return v.Html(
        tag = 'h3',
        children=[*([label] if label is not None else []), *children],
        class_=class_name,
        style_=style,
        **kwargs
    )

@widget.component
def h4(
    label: Optional[str] = None,
    children=[],
    class_name: str = '',
    style: str = '',
    **kwargs
):
    return v.Html(
        tag = 'h4',
        children=[*([label] if label is not None else []), *children],
        class_=class_name,
        style_=style,
        **kwargs
    )

@widget.component
def h5(
    label: Optional[str] = None,
    children=[],
    class_name: str = '',
    style: str = '',
    **kwargs
):
    return v.Html(
        tag = 'h5',
        children=[*([label] if label is not None else []), *children],
        class_=class_name,
        style_=style,
        **kwargs
    )

@widget.component
def h6(
    label: Optional[str] = None,
    children=[],
    class_name: str = '',
    style: str = '',
    **kwargs
):
    return v.Html(
        tag = 'h6',
        children=[*([label] if label is not None else []), *children],
        class_=class_name,
        style_=style,
        **kwargs
    )