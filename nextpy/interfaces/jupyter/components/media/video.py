import reacton.ipyvuetify as v
import nextpy.interfaces.jupyter as widget

@widget.component
def video(
    src: str = '',
    class_name: str = '',
    style: str = '',
    controls: bool = True,  # Show video controls
    autoplay: bool = True,  # Autoplay video
    loop: bool = False,  # Loop video
    **kwargs
):
    return v.Html(
        tag='video',
        attributes={
            'src': src,
            'controls': controls,
            'autoplay': autoplay,
            'loop': loop,
            **kwargs
        },
        children=[],
        class_=class_name,
        style_=style
    )
