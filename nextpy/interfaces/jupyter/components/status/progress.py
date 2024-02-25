from typing import Dict, List, Union

import reacton.ipyvuetify as v

import nextpy.interfaces.jupyter as widget
import nextpy.interfaces.jupyter.util


@widget.component
def progress(
    value: Union[bool, float] = True,
    color="primary",
    style: Union[str, Dict[str, str], None] = None,
    classes: List[str] = [],
):
    """Progress bar component showing a percentage, indeterminate or hidden.

     * When `value` is `True`, the progress bar will be indeterminate.
     * When `value` is `False`, the progress bar will be hidden, but still take up space.
       This can be used to avoid the page to jump when the progress bar is shown and hidden.
     * When `value` is a number between 0 and 100, the progress bar will show the percentage.

    ### Basic example

    ```widget
    import nextpy.interfaces.jupyter

    @widget.component
    def Page():
        widget.ProgressLinear(value=30, color="purple")
        widget.ProgressLinear(True)
    ```

    ## Arguments
     * `value`: Value of the progress bar. Can be a number between 0 and 100, `True` for indeterminate or `False` to hide.
     * `color`: Color of the progress bar.
     * `style`: CSS style to add to the progress bar.
     * `classes`: List of classes to apply to the progress bar.

    """
    indeterminate = value is True

    style_flat = widget.util._flatten_style(style)
    if value is False:
        style_flat = "visibility: hidden;" + style_flat
    class_ = widget.util._combine_classes(classes)
    v.ProgressLinear(indeterminate=indeterminate, value=value if value is not True else None, color=color, style_=style_flat, class_=class_)
