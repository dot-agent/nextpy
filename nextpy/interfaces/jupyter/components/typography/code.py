import reacton.ipyvuetify as v
from typing import List, Optional, Union
import nextpy.interfaces.jupyter as widget

@widget.component
def code(
    label: Optional[str] = None,
    children=[],
    class_name: str = '',
    style: str = '',
    **kwargs
):
    return v.Html(
        tag = 'pre',
        children=[*([label] if label is not None else []), *children],
        class_=class_name,
        style_=style,
        **kwargs
    )

# class CodeHighlightCssWidget(v.VuetifyTemplate):
#     template_file = (__file__, "code.vue")

# @widget.component
# def code_highlight():
#     return CodeHighlightCssWidget.element()