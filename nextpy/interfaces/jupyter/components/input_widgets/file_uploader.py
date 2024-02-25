import threading
import typing
from typing import Callable, Optional, cast

import traitlets
from ipyvue import Template
from ipyvuetify.extra import FileInput
from ipywidgets import widget_serialization
from typing_extensions import TypedDict

import nextpy.interfaces.jupyter as widget
import nextpy.interfaces.jupyter.hooks as hooks


class FileInfo(TypedDict):
    name: str
    size: int
    file_obj: typing.BinaryIO
    data: Optional[bytes]


class FileDropZone(FileInput):
    # override to narrow traitlet of FileInput
    template = traitlets.Instance(Template).tag(sync=True, **widget_serialization)
    template_file = (__file__, "file_drop.vue")
    items = traitlets.List(default_value=[]).tag(sync=True)
    label = traitlets.Unicode().tag(sync=True)


@widget.component
def file_dropper(
    label="Drop file here",
    on_total_progress: Optional[Callable[[float], None]] = None,
    on_file: Optional[Callable[[FileInfo], None]] = None,
    lazy: bool = True,
    class_name : str = '',
    style: str = ''
):
    """Region a user can drop a file into for file uploading.

    If lazy=True, no file content will be loaded into memory,
    nor will any data be transferred by default.
    A file object is passed to the `on_file` callback, and data will be transferred
    when needed.

    If lazy=False, the file content will be loaded into memory and passed to the `on_file` callback via the `.data` attribute.

    The on_file callback takes the following argument type:
    ```python
    class FileInfo(typing.TypedDict):
        name: str  # file name
        size: int  # file size in bytes
        file_obj: typing.BinaryIO
        data: Optional[bytes]: bytes  # only present if lazy=False
    ```


    ## Arguments
     * `on_total_progress`: Will be called with the progress in % of the file upload.
     * `on_file`: Will be called with a `FileInfo` object, which contains the file `.name`, `.length` and a `.file_obj` object.
     * `lazy`: Whether to load the file content into memory or not. If `False`,
        the file content will be loaded into memory and passed to the `on_file` callback via the `.data` attribute.

    """
    file_info, set_file_info = widget.use_state(None)
    wired_files, set_wired_files = widget.use_state(cast(Optional[typing.List[FileInfo]], None))

    file_drop = FileDropZone.element(label=label, on_total_progress=on_total_progress, on_file_info=set_file_info)  # type: ignore

    def wire_files():
        if not file_info:
            return

        real = cast(FileDropZone, widget.get_widget(file_drop))

        # workaround for @observe being cleared
        real.version += 1
        real.reset_stats()

        set_wired_files(cast(typing.List[FileInfo], real.get_files()))

    widget.use_side_effect(wire_files, [file_info])

    def handle_file(cancel: threading.Event):
        if not wired_files:
            return
        if on_file:
            if not lazy:
                wired_files[0]["data"] = wired_files[0]["file_obj"].read()
            else:
                wired_files[0]["data"] = None
            on_file(wired_files[0])

    result: widget.Result = hooks.use_thread(handle_file, [wired_files])
    if result.error:
        raise result.error

    return file_drop
