import warnings
from typing import Any, Callable, Dict, List, Union

import reacton
import reacton.ipyvuetify as v

import nextpy.interfaces.jupyter as widget
import nextpy.interfaces.jupyter.widgets
from nextpy.interfaces.jupyter.util import _combine_classes

Navigator = reacton.core.ComponentWidget(widget.widgets.Navigator)
GridDraggable = reacton.core.ComponentWidget(widget.widgets.GridLayout)
# keep the old name for a while
GridLayout = GridDraggable


@widget.component
def ListItem(title, icon_name: str = None, children=[], value=None):
    if value is None:
        value = title
    if children:
        with v.ListItemContent() as main:
            v.ListItemTitle(children=[title])
            if icon_name is not None:
                with v.ListItemIcon():
                    v.Icon(children=[icon_name or ""])
        return v.ListGroup(children=children, v_slots=[{"name": "activator", "children": main}], no_action=True, value=True, append_icon=icon_name)
    else:
        with v.ListItem(value=value) as main:
            if icon_name is not None:
                with v.ListItemIcon():
                    v.Icon(children=[icon_name or ""])
            with v.ListItemContent():
                v.ListItemTitle(children=[title])
        return main


def ui_dropdown(label, value=None, options=["foo", "bar"], key=None, disabled=False, **kwargs):
    key = key or str(value) + str(label) + str(options)
    value, set_value = widget.use_state(value, key)

    def set_index(index):
        set_value(options[index])

    v.Select(v_model=value, label=label, items=options, on_v_model=set_value, clearable=True, disabled=disabled, **kwargs)
    return value


def ui_text(label, value="", key=None, clearable=False, hint="", disabled=False, **kwargs):
    key = key or str(value) + str(label) + str(hint)
    value, set_value = widget.use_state(value, key)
    v.TextField(v_model=value, label=label, on_v_model=set_value, clearable=clearable, hint=hint, disabled=disabled, **kwargs)
    return value


def ui_checkbox(label, value=True, key=None, disabled=False, **kwargs):
    key = key or str(value) + str(label)
    value, set_value = widget.use_state(value, key)
    v.Checkbox(v_model=value, label=label, on_v_model=set_value, **kwargs)
    return value


def ui_slider(value=1, label="", min=0, max=100, key=None, tick_labels=None, thumb_label=None, disabled=False, **kwargs):
    key = key or str(value) + str(label)
    value, set_value = widget.use_state(value, key)
    v.Slider(
        v_model=value,
        label=label,
        min=min,
        max=max,
        on_v_model=set_value,
        ticks=tick_labels is not None,
        tick_labels=tick_labels,
        thumb_label=thumb_label,
        disabled=disabled,
        **kwargs,
    )
    return value


@widget.component
def text(text, style: Union[str, Dict[str, str], None] = None, classes: List[str] = []):
    style_flat = widget.util._flatten_style(style)
    return v.Html(tag="span", class_=_combine_classes(classes), style_=style_flat, children=[text])


@widget.component
def div(children=[], classes: List[str] = [], style: Union[str, Dict[str, str], None] = None, **kwargs):
    style_flat = widget.util._flatten_style(style)
    classes = classes.copy()
    kwargs = kwargs.copy()
    if "class_" in kwargs:
        classes.append(kwargs.pop("class_"))
    if "style_" in kwargs:
        style_flat += kwargs.pop("style_")
    class_ = _combine_classes(classes)

    return v.Html(tag="div", children=children, class_=class_, style_=style_flat, **kwargs)


@widget.component
def pre(text, **kwargs):
    return v.Html(tag="pre", children=[text], **kwargs)


@widget.component
def IconButton(icon_name: str = None, on_click=Callable[[], None], children: list = [], click_event="click", **kwargs):
    return widget.button(icon_name=icon_name, on_click=on_click, children=children, icon=True, click_event=click_event, **kwargs)


@widget.component
def html(tag="div", unsafe_innerHTML=None, style: str = None, classes: List[str] = [], attributes=None, class_: str = None):
    """Render an html tag with optional raw html text inside.

    # Arguments

     * `tag`: html tag name for the top level element (default: `div`)
     * `unsafe_innerHTML`: html string to be rendered inside the tag.
        Note that this is not sanitized, so be careful this cannot include JavaScript from user input!
     * `style`: CSS style string to be applied to the top level element.
     * `classes`: List of CSS classes to be applied to the top level element.
     * `attributes`: Dictionary of attributes to be applied to the top level element.
     * `class_`: (deprecated) CSS class to be applied to the top level element.

    """
    if attributes is None:
        attributes = {}
    else:
        attributes = attributes.copy()
    if style:
        attributes["style"] = style
    if class_ or classes:
        class_ = _combine_classes([*classes, *([] if class_ is None else [class_])])
        attributes["class"] = class_
    return widget.widgets.html.element(tag=tag, unsafe_innerHTML=unsafe_innerHTML, attributes=attributes)

@reacton.component
def head(children: List[reacton.core.Element] = []):
    """A component that manager the "head" tag of the page to avoid duplicate tags, such as titles.

    Currently only supports the [title](/api/title) tag as child, e.g.:

    ```python
    import nextpy.interfaces.jupyter

    @widget.component
    def Page():
        with widget.vstack() as main:
            MyAwesomeComponent()
            with widget.head():
                widget.Title("My page title")
        return main

    ```
    """
    return widget.div(children=children, style="display; none")

@widget.component
def vstack(children=[], grow=True, align_items="stretch", classes: List[str] = []):
    """Deprecated. Use `row` instead."""
    style = f"flex-direction: column; align-items: {align_items};"
    if grow:
        style += "flex-grow: 1;"
    class_ = _combine_classes(["d-flex", *classes])
    return v.Sheet(class_=class_, style_=style, elevation=0, children=children)


@widget.component
def hstack(children=[], grow=True, align_items="stretch", classes: List[str] = []):
    """Deprecated. Use `column` instead."""
    style = f"flex-direction: row; align-items: {align_items}; "
    if grow:
        style += "flex-grow: 1;"
    class_ = _combine_classes(["d-flex", *classes])
    return v.Sheet(class_=class_, style_=style, elevation=0, children=children)


@widget.component
def row(children=[], gap="12px", justify="start", margin: int = 0, classes: List[str] = [], style: Union[str, Dict[str, str], None] = None):
    """Lays out children in a row, side by side, with the given gap between them.

    See also [column](/api/column).

    Example with three children side by side:

    ```widget
    import nextpy.interfaces.jupyter

    @widget.component
    def Page():
        with widget.row(gap="10px", justify="space-around"):
            widget.text("On the left")
            widget.text("In the middle")
            widget.text("On the right")
    ```
    ## Arguments

     * `children`: List of children to render in the column.
     * `gap`: The gap between each child, as a CSS string.
     * `justify`: How children are distributed along the x/horizontal-axis, can be "start" (default), "center", "end", "space-around",
        "space-between" or "space-evenly".
        (*Note: this translates to justify-content in CSS*).
     * `margin`: The margin around the column, translate to 4*margin pixels.
     * `classes`: List of CSS classes to apply to the column.
     * `style`: CSS style to apply to the column.

    """
    align_items = "stretch"
    style_flat = widget.util._flatten_style(style)
    style_flat = f"flex-direction: row; align-items: {align_items}; justify-content: {justify}; column-gap: {gap};" + style_flat + ";"
    # valid css values, but we don't list them as options to avoid confusion
    extra_justify_options = ["left", "right", "flex-start", "flex-end"]
    if justify not in (["start", "center", "end", "space-around", "space-between", "space-evenly"] + extra_justify_options):
        warnings.warn(f"Invalid value for justify: {justify}, possible values are: start, center, end, space-around, space-between, space-evenly")
    class_ = _combine_classes(["d-flex", f"ma-{margin}", *classes])
    return v.Sheet(class_=class_, style_=style_flat, elevation=0, children=children)


@widget.component
def column(children=[], gap="12px", align="stretch", margin: int = 0, classes: List[str] = [], style: Union[str, Dict[str, str], None] = None):
    """Lays out children in a column on top of each other, with the given gap between them.

    See also [row](/api/row).

    Example with three children on top of each other:

    ```widget
    import nextpy.interfaces.jupyter

    @widget.component
    def Page():
        with widget.column(gap="10px"):
            widget.text("On top")
            widget.text("In the middle")
            widget.text("On bottom")
    ```

    ## Arguments

     * `children`: List of children to render in the column.
     * `gap`: The gap between each child, as a CSS string.
     * `align`: The alignment of the children, can be "start", "center", "end", "stretch" (default).
        (*Note: this translates to align-items in CSS*).
     * `margin`: The margin around the column, translate to 4*margin pixels.
     * `classes`: List of CSS classes to apply to the column.
     * `style`: CSS style to apply to the column.

    """
    if align == "left":
        warnings.warn("align='left' does not exists, you probably want align='start' instead")
        align = "start"
    if align == "right":
        warnings.warn("align='right' does not exists, you probably want align='end' instead")
        align = "end"
    # valid css options, but we don't list them as options to avoid confusion
    extra_align_options = ["flex-start", "flex-end", "self-start", "self-end", "baseline"]
    if align not in (["start", "center", "end", "stretch"] + extra_align_options):
        warnings.warn(f"Invalid value for align: {align}, possible values are 'start', 'center', 'end' or 'stretch'")
    style_flat = widget.util._flatten_style(style)
    style_flat = f"flex-direction: column; align-items: {align}; row-gap: {gap};" + style_flat + ";"
    class_ = _combine_classes(["d-flex", f"ma-{margin}", *classes])
    return v.Sheet(class_=class_, style_=style_flat, elevation=0, children=children)


@widget.component
def GridFixed(columns=4, column_gap="10px", row_gap="10px", children=[], align_items="stretch", justify_items="stretch"):
    """

    See css grid spec:
    https://css-tricks.com/snippets/css/complete-guide-grid/
    """
    style = (
        f"display: grid; grid-template-columns: repeat({columns}, minmax(0, 1fr)); "
        + f"grid-column-gap: {column_gap}; grid-row-gap: {row_gap}; align-items: {align_items}; justify-items: {justify_items}"
    )
    return div(style_=style, children=children)


@widget.component
def padding(size, children=[], grow=True):
    style = "flex-direction: row;"
    if grow:
        style += "flex-grow: 1;"
    return v.Sheet(class_=f"pa-{size}", style_=style, elevation=0, children=children)


@widget.component
def FigurePlotly(
    fig,
    on_selection: Callable[[Any], None] = None,
    on_deselect: Callable[[Any], None] = None,
    on_click: Callable[[Any], None] = None,
    on_hover: Callable[[Any], None] = None,
    on_unhover: Callable[[Any], None] = None,
    on_relayout: Callable[[Any], None] = None,
    dependencies=None,
):
    from plotly.graph_objs._figurewidget import FigureWidget

    def on_points_callback(data):
        if not data:
            return

        event_type = data["event_type"]
        event_mapping = {
            "plotly_click": on_click,
            "plotly_hover": on_hover,
            "plotly_unhover": on_unhover,
            "plotly_selected": on_selection,
            "plotly_deselect": on_deselect
        }
        
        callback = event_mapping.get(event_type)
        if callback:
            callback(data)

    fig_element = FigureWidget.element(
        on__js2py_pointsCallback=on_points_callback,
        on__js2py_relayout=on_relayout
    )

    def update_data():
        fig_widget: FigureWidget = widget.get_widget(fig_element)
        fig_widget.layout = fig.layout

        length = len(fig_widget.data)
        fig_widget.add_traces(fig.data)
        data = list(fig_widget.data)
        fig_widget.data = data[length:]

    widget.use_effect(update_data, dependencies or fig)
    return fig_element


@widget.component
def Code(path, path_header=None):
    path_header = path_header or path
    with open(path) as f:
        code = f.read()
    md = widget.Markdown(
        f"""
### {path_header}

```python
{code}
```

"""
    )

    with v.ExpansionPanels() as main:
        with v.ExpansionPanel():
            with v.ExpansionPanelHeader(children=["View source"]):
                pass
            with v.ExpansionPanelContent(children=[md]):
                pass
    return main
