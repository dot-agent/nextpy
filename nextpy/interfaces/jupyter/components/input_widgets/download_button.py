from pathlib import Path
from typing import BinaryIO, Callable, Optional, Union, cast

import ipyvuetify as vy
import ipywidgets as widgets
import traitlets

import nextpy.interfaces.jupyter as widget


class FileDownloadWidget(vy.VuetifyTemplate):
    template_file = (__file__, "download.vue")
    children = traitlets.List().tag(sync=True, **widgets.widget_serialization)
    filename = traitlets.Unicode().tag(sync=True)
    bytes = traitlets.Bytes(None, allow_none=True).tag(sync=True)
    mime_type = traitlets.Unicode("application/octet-stream").tag(sync=True)
    request_download = traitlets.Bool(False).tag(sync=True)


@widget.component
def download_button(
    data: Union[str, bytes, BinaryIO, Callable[[], Union[str, bytes, BinaryIO]]],
    filename: Optional[str] = None,
    label: Optional[str] = None,
    icon_name: Optional[str] = "mdi-cloud-download-outline",
    close_file: bool = True,
    type: str = "application/octet-stream",
    string_encoding: str = "utf-8",
    children=[],
    class_name : str = '',
    style: str = ''
):
    """Download a file or data.

    ## Simple usage

    By default, if no children are provided, a button is created with the label "Download: {filename}".

    ```widget
    import nextpy.interfaces.jupyter

    data = "This is the content of the file"

    @widget.component
    def Page():
        widget.FileDownload(data, filename="widget-download.txt", label="Download file")
    ```

    ## Advanced usage

    If children are provided, they are displayed instead of the button. The children can be any widget component,
    including a button, markdown text, or an image.

    ```widget
    import nextpy.interfaces.jupyter

    data = "This is the content of the file"

    @widget.component
    def Page():
        with widget.FileDownload(data, "widget-download-2.txt"):
            widget.Markdown("Any text, or even an image")
            widget.Image("https://widget.dev/static/public/beach.jpeg", width="200px")
    ```

    ## Custom button

    If children are provided, they are displayed instead of the button. The children can be any widget component,
    including a button, markdown text, or an image.

    ```widget
    import nextpy.interfaces.jupyter

    data = "This is the content of the file"

    @widget.component
    def Page():
        with widget.FileDownload(data, "widget-download-2.txt"):
            widget.button("Custom download button", icon_name="mdi-cloud-download-outline", color="primary")
    ```

    ## Usage with file

    A file object can be used as data. The file will be closed after downloading by default.

    ```widget
    import nextpy.interfaces.jupyter
    import pandas as pd

    df = pd.DataFrame({"id": [1, 2, 3], "name": ["John", "Mary", "Bob"]})

    @widget.component
    def Page():
        file_object = df.to_csv(index=False)
        widget.FileDownload(file_object, "users.csv", mime_type="application/vnd.ms-excel")
    ```

    If a file like object is used, we try to base the filename on the file object.
    ```widget
    import nextpy.interfaces.jupyter
    import nextpy.interfaces.jupyter.website.pages
    import os

    filename = os.path.dirname(widget.website.__file__) + "/public/beach.jpeg"

    @widget.component
    def Page():
        # only open the file once by using use_memo
        file_object = widget.use_memo(lambda: open(filename, "rb"), [])
        # no filename is provided, but we can extract it from the file object
        widget.FileDownload(file_object, mime_type="image/jpeg", close_file=False)
    ```

    ## Lazy reading

    Not only is the data lazily uploaded to the browser, but also the data is only read when the download is requested.
    This happens for files by default, but can also be used by passing in a callback function.

    ```widget
    import nextpy.interfaces.jupyter
    import time

    @widget.component
    def Page():
        def get_data():
            # I run in a thread, so I can do some heavy processing
            time.sleep(3)
            # I only get called when the download is requested
            return "This is the content of the file"
        widget.FileDownload(get_data, "widget-lazy-download.txt")
    ```

    ## Arguments

     * `data`: The data to download. Can be a string, bytes, or a file like object, or a function that returns one of these.
     * `filename`: The name of the file the user will see as default when downloading (default name is "widget-download.dat").
        If a file object is provided, the filename will be extracted from the file object if possible.
     * `label`: The label of the button. If not provided, the label will be "Download: {filename}".
     - `icon_name`: The name of the icon to display on the button ([Overview of available icons](https://pictogrammers.github.io/@mdi/font/4.9.95/)).
     * `close_file`: If a file object is provided, close the file after downloading (default True).
     * `mime_type`: The mime type of the file. If not provided, the mime type will be "application/octet-stream",
           For instance setting it to "application/vnd.ms-excel" will allow the user OS to directly open the
           file into Excel.
     * `string_encoding`: The encoding to use when converting a string to bytes (default "utf-8").

    ## Note on file size

    Note that the data will be kept in memory when downloading.
    If the file is large (>10 MB), and when using [Solara server](/docs/understanding), we recommend using the
    [static files directory](/docs/reference/static-files) instead.

    """
    request_download, set_request_download = widget.use_state(False)

    # if the data changes, we 'reset'
    def reset():
        nonlocal request_download
        request_download = False
        set_request_download(False)

    widget.use_memo(reset, [data])

    # we only upload to the frontend if clicked
    def get_data() -> Optional[bytes]:
        if request_download:
            if callable(data):
                data_non_lazy = data()
            else:
                data_non_lazy = data
            if hasattr(data_non_lazy, "read"):
                if hasattr(data_non_lazy, "seek"):
                    if hasattr(data_non_lazy, "tell") and data_non_lazy.tell() != 0:
                        data_non_lazy.seek(0)
                content = data_non_lazy.read()  # type: ignore
                if close_file:
                    data_non_lazy.close()  # type: ignore
                return content
            elif isinstance(data_non_lazy, str):
                return data_non_lazy.encode(string_encoding)
            else:
                return cast(bytes, data_non_lazy)
        return None

    bytes_result: widget.Result[Optional[bytes]] = widget.use_thread(get_data, dependencies=[request_download, data])
    if filename is None and hasattr(data, "name"):
        try:
            filename = Path(data.name).name  # type: ignore
        except Exception:
            pass
    filename = filename or "downloaded.dat"
    label = label or ("Download")
    FileDownloadWidget.element(
        filename=filename,
        bytes=bytes_result.value if bytes_result.state == widget.ResultState.FINISHED else None,
        request_download=request_download,
        on_request_download=set_request_download,
        children=children or [widget.button(label, loading=bytes_result.state == widget.ResultState.RUNNING, icon_name=icon_name)],
        mime_type=type,
        class_=class_name,
        style_=style 
    )
    if bytes_result.state == widget.ResultState.ERROR and bytes_result.error:
        raise bytes_result.error
