import reacton.ipyvuetify as v
import nextpy.interfaces.jupyter as widget

@widget.component
def form(
    action: str = '#',
    method: str = 'post',
    class_name: str = '',
    style: str = '',
    **kwargs
):
    return v.Html(
        tag='form', 
        attributes={'action': action, 'method': method, **kwargs},
        class_=class_name, 
        style_=style
    )

