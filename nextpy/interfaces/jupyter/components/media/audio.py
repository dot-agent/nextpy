import reacton.ipyvuetify as v
import nextpy.interfaces.jupyter as widget

@widget.component
def audio(
    src: str = '',
    class_name: str = '',
    style: str = '',
    **kwargs
):
    return v.Html(
        tag='audio', 
        attributes={
            'controls': True,
            'src': src,
            **kwargs
        }, 
        class_=class_name, 
        style_=style
    )

