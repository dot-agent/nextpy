from typing import Optional, Union

import reacton.ipyvuetify as v

import nextpy.interfaces.jupyter as widget


@widget.component
def tooltip(
    tooltip=Union[str, widget.Element],
    children=[],
    color: Optional[str] = None,
):
    """A tooltip that is shown when you hover above an element.

    Not all components support tooltips, in case it does not work,
    try wrapping the element in a `column` or `row`.

    ```widget
    import nextpy.interfaces.jupyter

    @widget.component
    def Page():
        with widget.Tooltip("This is a tooltip over a button"):
            widget.button("Hover me")
        with widget.Tooltip("This is a tooltip over a text"):
            widget.text("Hover me")
        info = widget.Info("Any component is supported as tooltip.")
        with widget.Tooltip(info, color="white"):
            with widget.column():
                widget.Markdown("# Lorem ipsum\\n\\nDolor sit amet")
    ```

    ## Arguments

     * `tooltip`: the text, or element to display on hover.
     * `children`: the element to display the tooltip over.
     * `color`: the color of the tooltip (if None, the default color).

    """

    def set_v_on():
        for child in children:
            widget = widget.get_widget(child)
            # this only works on vue/vuetify components
            widget.v_on = "tooltip.on"  # type: ignore

    widget.use_effect(set_v_on, children)

    return v.Tooltip(
        bottom=True,
        v_slots=[
            {
                "name": "activator",
                "variable": "tooltip",
                "children": children,
            }
        ],
        color=color,
        children=[tooltip],
    )
