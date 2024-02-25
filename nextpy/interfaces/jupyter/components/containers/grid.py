import itertools
from typing import Dict, List, Union

import reacton.ipyvuetify as rv

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.util import _combine_classes


def cycle(value):
    if value is None:
        return itertools.cycle([None])
    elif isinstance(value, int):
        return itertools.cycle([value])
    elif isinstance(value, (list, tuple)):
        return itertools.cycle(value)
    else:
        raise ValueError(f"Invalid value for columns: {value}, should be None, int, or list/tuple.")


@widget.component
def grid(
    widths: List[Union[float, int]] = [1],
    wrap=True,
    gutters=True,
    gutters_dense=False,
    children=[],
    class_name: str = '',
    style: Union[str, Dict[str, str], None] = None,
):
    """Lays out children in columns, with relative widths specified as a list of floats or ints.

    Widths are relative to each other, so [1, 2, 1] will result in 1/4, 1/2, 1/4 width columns.
    columns with a width of 0 will take up the minimal amount of space.

    If there are more children than widths, the width list will be cycled.

    ```python
    with widget.columns([1, 2, 1]):
        widget.text("I am on the left")
        with widget.Card("Middle"):
            ...
        with widget.column():
            ...
    ```

    When three children are added to this component, they will be laid out in three columns,
    with the first and last column taking up 1/4 of the width, and the middle column taking up 1/2 of the width.

    ```widget
    import nextpy.interfaces.jupyter

    @widget.component
    def Page():
        with widget.columns([0, 1, 2]):
            widget.text("I am as small as possible")
            widget.Select("I stretch", values=["a", "b", "c"], value="a")
            widget.Select("I stretch twice the amount", values=["a", "b", "c"], value="a")
    ```


    # Arguments

     * `widths`: List of floats or ints, specifying the relative widths of the columns.
     * `wrap`: Whether to wrap the columns to the next row if there is not enough space available. This only happens when using widths of 0.
     * `gutters`: Whether to add gutters between the columns.
     * `gutters_dense`: Make gutters smaller.
     * `children`: List of children to be laid out in columns.
     * `style`: CSS style to apply to the top level element.
     * `classes`: List of CSS classes to be applied to the top level element.

    """
    class_ = _combine_classes([*(["flex-nowrap"] if not wrap else []), class_name])
    style_flat = widget.util._flatten_style(style)
    with rv.Row(class_=class_, no_gutters=not gutters, dense=gutters_dense, style_=style_flat) as main:
        for child, width in zip(children, cycle(widths)):
            # we add height: 100% because this will trigger a chain of height set if it is set on the parent
            # via the style. If we do not set the height, it will have no effect. Furthermore, we only have
            # a single child, so this cannot interfere with other siblings.
            with rv.Col(children=[child], style_=f"height: 100%; flex-grow: {width}; overflow: auto" if width != 0 else "flex-grow: 0"):
                pass
    return main


@widget.component
def responsive_grid(
    default=None,
    small=None,
    medium=None,
    large=None,
    xlarge=None,
    children=[],
    wrap=True,
    gutters=True,
    gutters_dense=False,
    class_name: str = '',
    style: Union[str, Dict[str, str], None] = None,
):
    """Lay our children in columns, on a 12 point grid system that is responsive to screen size.

    If a single number is specified, or less values than children, the values will be cycled.
    The total width of this system is 12, so if you want to have 3 columns, each taking up 4 points, you would specify [4, 4, 4] or 4.


    ```python
    with columnsResponsive([4, 4, 4]):
        ...
    with columnsResponsive(4):  # same effect
        ...
    ```

    If you want the first column to take up 4 points, and the second column to take up the remaining 8 points, you would specify [4, 8].

    ```python
    with columnsResponsive([4, 8]):
        ...
    ```

    If you want your columns to be full width on large screen, and next to each other on larger screens.

    ```python
    with columnsResponsive(12, large=[4, 8]):
        ...
    ```

    # Arguments

     * default: Width of column for >= 0 px.
     * small: Width of column for >= 600 px.
     * medium: Width of column >= 960 px.
     * large: Width of column for >= 1264 px.
     * xlarge: Width of column for >= 1904 px.

    """

    def cycle(value):
        if value is None:
            return itertools.cycle([None])
        elif isinstance(value, int):
            return itertools.cycle([value])
        elif isinstance(value, (list, tuple)):
            return itertools.cycle(value)
        else:
            raise ValueError(f"Invalid value for columns: {value}, should be None, int, or list/tuple.")

    class_ = _combine_classes([*(["flex-nowrap"] if not wrap else []), class_name])
    style_flat = widget.util._flatten_style(style)
    with rv.Row(class_=class_ if not wrap else "", style_=style_flat, no_gutters=not gutters, dense=gutters_dense) as main:
        for child, xsmall, small, medium, large, xlarge in zip(children, cycle(default), cycle(small), cycle(medium), cycle(large), cycle(xlarge)):
            with rv.Col(
                cols=xsmall,
                sm=small,
                md=medium,
                lg=large,
                xl=xlarge,
                children=[child],
            ):
                pass
    return main
