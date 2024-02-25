import reacton.ipyvuetify as v
from typing import Optional, Union, Callable, List, Dict
import nextpy.interfaces.jupyter as widget

@widget.component
def radio(
    label: Optional[str] = None,
    options: List[str] = [],
    value: Optional[str] = None,
    key: Optional[Union[str, int]] = None,
    help: Optional[str] = None,
    on_change: Optional[Callable] = None,
    args: Optional[Dict] = None,
    kwargs: Optional[Dict] = None,
    disabled: bool = False,
    horizontal: bool = False,
    class_name: str = '',
    style: str = '',
    icons: Optional[List[str]] = None,
    label_visibility: str = "visible",
):
    if kwargs is None:
        kwargs = {}
    if label_visibility == "hidden":
        label = ""
    elif label_visibility == "collapsed":
        class_name += " no-label"

    radio_buttons = [
        v.Radio(label=f"{option} {icons[idx] if icons else ''}", value=option, disabled=disabled)
        for idx, option in enumerate(options)
    ]

    radio_group = v.RadioGroup(
        v_model=value,
        children=radio_buttons,
        row=horizontal,
        class_=class_name,
        style_=style,
        **kwargs
    )
    if on_change:
        radio_group.on_event('change', lambda *args, **kwargs: on_change(*args, **kwargs))

    container = v.Container(children=[v.Html(tag='h3', children=[label]), radio_group])

    return container
