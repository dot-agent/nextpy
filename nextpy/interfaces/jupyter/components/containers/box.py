import reacton.ipyvuetify as v
import nextpy.interfaces.jupyter as widget

@widget.component
def box(
    children: list = [],
    class_name: str = '',
    style:str = '',
    **kwargs,
):
    return v.Html(
        tag='div',
        children=children,
        class_=class_name,
        style_=style,
        **kwargs,
    )