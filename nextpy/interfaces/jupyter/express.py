import functools
import typing
from typing import Callable

import numpy as np
import plotly.express as px
import plotly.graph_objs as go
import typing_extensions

# behave as the px module
from plotly.express import *  # noqa: F401, F403
from plotly.express._core import make_figure

import nextpy.interfaces.jupyter as widget

P = typing_extensions.ParamSpec("P")
T = typing.TypeVar("T")
T2 = typing.TypeVar("T2")


# patch histogram until issue 3859 in plotly is resolved


def histogram(
    data_frame=None,
    x=None,
    y=None,
    custom_data=None,
    color=None,
    pattern_shape=None,
    facet_row=None,
    facet_col=None,
    facet_col_wrap=0,
    facet_row_spacing=None,
    facet_col_spacing=None,
    hover_name=None,
    hover_data=None,
    animation_frame=None,
    animation_group=None,
    category_orders=None,
    labels=None,
    color_discrete_sequence=None,
    color_discrete_map=None,
    pattern_shape_sequence=None,
    pattern_shape_map=None,
    marginal=None,
    opacity=None,
    orientation=None,
    barmode="relative",
    barnorm=None,
    histnorm=None,
    log_x=False,
    log_y=False,
    range_x=None,
    range_y=None,
    histfunc=None,
    cumulative=None,
    nbins=None,
    text_auto=False,
    title=None,
    template=None,
    width=None,
    height=None,
) -> go.Figure:
    """
    In a histogram, rows of `data_frame` are grouped together into a
    rectangular mark to visualize the 1D distribution of an aggregate
    function `histfunc` (e.g. the count or sum) of the value `y` (or `x` if
    `orientation` is `'h'`).
    """
    return make_figure(
        args=locals(),
        constructor=go.Histogram,
        trace_patch=dict(
            histnorm=histnorm,
            histfunc=histfunc,
            cumulative=dict(enabled=cumulative),
        ),
        layout_patch=dict(barmode=barmode, barnorm=barnorm),
    )


px.histogram = histogram


def _make_self_describing(f: Callable[P, T]):
    # put the arguments on the function and the function into the return value
    @functools.wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        fig = f(*args, **kwargs)
        fig._func = f  # type: ignore
        fig._args = args  # type: ignore
        fig._kwargs = kwargs  # type: ignore
        return fig

    return wrapper


def _patch():
    for name in dir(px):
        f = getattr(px, name)
        if callable(f):
            f = _make_self_describing(f)
            setattr(px, name, f)


_patch()


@widget.component
def CrossFilteredFigurePlotly(fig):
    first_arg_name = fig._func.__code__.co_varnames[0]
    kwargs = fig._kwargs.copy()
    kwargs.update(zip(fig._func.__code__.co_varnames, fig._args))

    df = kwargs[first_arg_name]
    name = fig._func.__name__
    filter, set_filter = widget.use_cross_filter(id(df), name)
    dff = df
    if filter is not None:
        dff = df[filter]
        for key, value in kwargs.items():
            if not isinstance(value, str):
                try:
                    n = len(value)
                except TypeError:
                    pass  # int or bool, or anything without a length
                except Exception:
                    raise
                else:
                    if n == len(df):
                        kwargs[key] = np.array(value)[filter]
        original_indices = np.arange(len(df), dtype="int64")
    else:
        original_indices = None

    kwargs[first_arg_name] = dff

    index = np.arange(len(dff))
    custom_data = [index]
    has_custom_data = "custom_data" in kwargs

    if has_custom_data:
        kwargs["custom_data"] = custom_data + list(kwargs["custom_data"])
    else:
        kwargs["custom_data"] = custom_data
    new_fig = fig._func(**kwargs)
    new_fig.layout = fig.layout

    # the df is split into multiple traces, generate the data such that we can transform back from trace+point indices to df.index
    indices = []
    offset = 0
    index_offsets_list = []
    for data in new_fig.data:
        indices.append(data.customdata.T[0])
        index_offsets_list.append(offset)
        offset += len(data.customdata.T[0])
    index_offsets = np.array(index_offsets_list)
    # strip of the custom data we added
    for data in new_fig.data:
        if has_custom_data:
            data.customdata = data.customdata.T[len(custom_data) :].T
        else:
            data.customdata = None

    def on_selection(data):
        if data is not None:
            trace_indexes = np.array(data["points"]["trace_indexes"])
            point_indexes = np.array(data["points"]["point_indexes"])
            if len(trace_indexes):
                indices_selected = index_offsets[trace_indexes] + point_indexes

                if filter is not None:
                    assert original_indices is not None
                    # these are references to the filtered dataframe
                    indices_selected = original_indices[filter][indices_selected]
                mask = np.zeros(len(df), dtype=bool)
                mask[indices_selected] = True
                set_filter(mask)
            else:
                set_filter(None)

    def on_deselect(data):
        set_filter(None)

    return widget.FigurePlotly(new_fig, on_selection=on_selection, on_deselect=on_deselect)


# for backwards compatibility
FigurePlotlyCrossFiltered = CrossFilteredFigurePlotly


def _wraps(f: Callable[P, T]):
    @functools.wraps(f)
    def wrapper(*args: P.args, **kwargs: P.kwargs):
        fig = f(*args, **kwargs)
        return CrossFilteredFigurePlotly(fig)

    return wrapper


scatter = _wraps(px.scatter)
scatter_3d = _wraps(px.scatter_3d)
scatter_polar = _wraps(px.scatter_polar)
scatter_ternary = _wraps(px.scatter_ternary)
scatter_mapbox = _wraps(px.scatter_mapbox)
scatter_geo = _wraps(px.scatter_geo)
scatter_matrix = _wraps(px.scatter_matrix)
density_contour = _wraps(px.density_contour)
density_heatmap = _wraps(px.density_heatmap)
density_mapbox = _wraps(px.density_mapbox)
line = _wraps(px.line)
line_3d = _wraps(px.line_3d)
line_polar = _wraps(px.line_polar)
line_ternary = _wraps(px.line_ternary)
line_mapbox = _wraps(px.line_mapbox)
line_geo = _wraps(px.line_geo)
parallel_coordinates = _wraps(px.parallel_coordinates)
parallel_categories = _wraps(px.parallel_categories)
area = _wraps(px.area)
bar = _wraps(px.bar)
timeline = _wraps(px.timeline)
bar_polar = _wraps(px.bar_polar)
violin = _wraps(px.violin)
box = _wraps(px.box)
strip = _wraps(px.strip)
histogram = _wraps(px.histogram)
ecdf = _wraps(px.ecdf)
choropleth = _wraps(px.choropleth)
choropleth_mapbox = _wraps(px.choropleth_mapbox)
pie = _wraps(px.pie)
sunburst = _wraps(px.sunburst)
treemap = _wraps(px.treemap)
icicle = _wraps(px.icicle)
funnel = _wraps(px.funnel)
funnel_area = _wraps(px.funnel_area)
imshow = _wraps(px.imshow)
