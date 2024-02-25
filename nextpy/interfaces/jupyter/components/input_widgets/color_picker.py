import reacton.ipyvuetify as v
from typing import Optional, Union, Callable, Tuple, Dict
import nextpy.interfaces.jupyter as widget

@widget.component
def color_picker(
    label: Optional[str] = None,
    value: Optional[str] = None,
    key: Optional[Union[str, int]] = None,
    help: Optional[str] = None,
    on_change: Optional[Callable] = None,
    args: Optional[Tuple] = None,
    kwargs: Optional[Dict] = None,
    disabled: bool = False,
    label_visibility: str = "visible",
    class_name: str = '',
    style: str = '',
):
    if kwargs is None:
        kwargs = {}
    if label_visibility == "hidden":
        label = ""
    elif label_visibility == "collapsed":
        class_name += " no-label"

    if value is None:
        value = "#000000"  

    component_kwargs = {
        "v_model": value,
        "class_": class_name,
        "style_": style,
        "disabled": disabled,
        "label": label,
        **kwargs
    }

    if on_change:
        component_kwargs["on_v_model"] = lambda *args, **kwargs: on_change(*args, **kwargs)

    return v.ColorPicker(**component_kwargs)
