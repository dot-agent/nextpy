import io
from typing import Any, List

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.alias import rw


@widget.component
def matplotlib(
    figure,
    dependencies: List[Any] = None,
    format: str = "svg",
    **kwargs,
):
    """Display a matplotlib figure.

    We recomment not to use the pyplot interface, but rather to create a figure directly, e.g:

    ```python
    import reacton
    import nextpy.interfaces.jupyter as sol
    from matplotlib.figure import Figure

    @widget.component
    def Page():
        # do this instead of plt.figure()
        fig = Figure()
        ax = fig.subplots()
        ax.plot([1, 2, 3], [1, 4, 9])
        return widget.matplotlib(fig)

    ```

    You should also avoid drawing using the pyplot interface, as it is not thread-safe. If you do use it,
    your drawing might be corrupted due to another thread/user drawing at the same time.

    If you still must use pyplot to create the figure, make sure you call `plt.switch_backend("agg")`
    before creating the figure, to avoid starting an interactive backend.

    For performance reasons, you might want to pass in a list of dependencies that indicate when
    the figure changed, to avoid re-rendering it on every render.


    ## Arguments

     * `figure`: Matplotlib figure.
     * `dependencies`: List of dependencies to watch for changes, if None, will convert the figure to a static image on each render.
     * `format`: The image format to to convert the Matplotlib figure to (png, jpg, svg, etc.)
     * `kwargs`: Additional arguments to passed to figure.savefig
    """

    def make_image():
        f = io.BytesIO()
        figure.savefig(f, format=format, **kwargs)
        return f.getvalue()

    value = widget.use_memo(make_image, dependencies)
    # mime type name is different from format name of matplotlib
    format_mime = format
    if format_mime == "svg":
        format_mime = "svg+xml"
    return rw.Image(value=value, format=format_mime)
