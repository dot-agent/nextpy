import reacton.ipyvuetify as v
import nextpy.interfaces.jupyter as widget

@widget.component
def image(
    src: str,  
    alt: str = '',
    class_name: str = '',
    style: str = '',
    **kwargs
):
    return v.Html(
        tag='img',
        attributes={
            'src': src,
            'alt': alt,
            **kwargs
        },
        class_=class_name,
        style_=style
    )