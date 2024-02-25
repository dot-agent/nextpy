import reacton.ipyvuetify as v
from typing import Optional, Union, Callable, Tuple, Dict
import nextpy.interfaces.jupyter as widget

@widget.component
def textarea(
    label: Optional[str] = None,
    value: str = "",
    max_chars: Optional[int] = None,
    key: Optional[Union[str, int]] = None,
    type: str = "default",
    help: Optional[str] = None,
    autocomplete: Optional[str] = None,
    on_change: Optional[Callable] = None,
    args: Optional[Tuple] = None,
    kwargs: Optional[Dict] = None,
    placeholder: Optional[str] = None,
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

    component_kwargs = {
        "label": label,
        "v_model": value,
        "maxlength": max_chars,
        "type": type,
        "hint": help,
        "persistent_hint": True,
        "placeholder": placeholder,
        "disabled": disabled,
        "class_": class_name,
        "style_": style,
        **kwargs
    }

    if on_change:
        component_kwargs["on_change"] = lambda *args, **kwargs: on_change(*args, **kwargs)

    return v.Textarea(**component_kwargs)
