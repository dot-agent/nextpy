import dataclasses
import io
import json
import logging
import os

# import tempfile
import threading
import time
import urllib.request
import uuid
from typing import IO, Any, Callable, Tuple, TypeVar, Union, cast

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.datatypes import FileContentResult, Result

logger = logging.getLogger("react-ipywidgets.extra.hooks")
chunk_size_default = 1024**2

__all__ = [
    "use_download",
    "use_fetch",
    "use_json_load",
    "use_json",
    "use_file_content",
    "use_uuid4",
    "use_unique_key",
    "use_state_or_update",
    "use_previous",
]
T = TypeVar("T")
U = TypeVar("U")

MaybeResult = Union[T, Result[T]]


def use_retry(*actions: Callable[[], Any]):
    counter, set_counter = widget.use_state(0)

    def retry():
        for action in actions:
            action()
        set_counter(lambda counter: counter + 1)

    return counter, retry


def use_download(
    f: MaybeResult[Union[str, os.PathLike, IO]], url, expected_size=None, delay=None, return_content=False, chunk_size=chunk_size_default
) -> Result:
    from .use_thread import use_thread

    if not isinstance(f, Result):
        f = Result(value=f)
    assert isinstance(f, Result)
    content_length, set_content_length = widget.use_state(expected_size, key="content_length")
    downloaded_length = 0
    file_object = hasattr(f.value, "tell")
    if not file_object:
        file_path = cast(Union[str, os.PathLike], f.value)
        if os.path.exists(file_path) and expected_size is not None:
            file_size = os.path.getsize(file_path)
            if file_size == expected_size:
                downloaded_length = file_size
    downloaded_length, set_downloaded_length = widget.use_state(downloaded_length, key="downloaded_length")

    def download(cancel: threading.Event):
        assert isinstance(f, Result)
        nonlocal downloaded_length
        if expected_size is not None and downloaded_length == expected_size:
            return  # we already downloaded, but hooks cannot be conditional

        context: Any = None
        if file_object:
            context = widget.util.nullcontext()
            output_file = cast(IO, f.value)
        else:
            # f = cast(Result[Union[str, os.PathLike]], f)
            output_file = context = open(f.value, "wb")  # type: ignore

        with context:
            with urllib.request.urlopen(url) as response:
                content_length = int(response.info()["Content-Length"])
                logger.info("content_length for %r = %r", url, content_length)
                set_content_length(content_length)
                bytes_read = 0
                while not cancel.is_set():
                    chunk = response.read(chunk_size)

                    if delay:
                        time.sleep(delay)
                    if not chunk:
                        break
                    bytes_read += len(chunk)
                    output_file.write(chunk)
                    set_downloaded_length(bytes_read)
        return bytes_read

    result: Result[Any] = use_thread(download, [f, url])
    # maybe we wanna check this
    # download_is_done = downloaded_length == content_length

    if content_length is not None:
        progress = downloaded_length / content_length
    else:
        progress = 0

    return dataclasses.replace(result, progress=progress)


def use_fetch(url, chunk_size=chunk_size_default):
    # re-use the same file like object
    f = widget.use_memo(io.BytesIO, [url])
    result = use_download(f, url, return_content=True, chunk_size=chunk_size)
    return dataclasses.replace(result, value=f.getvalue() if result.progress == 1 else None)


def compose_result(head, *tail):
    return head


def ensure_result(input: MaybeResult[T]) -> Result[T]:
    if isinstance(input, Result):
        return input
    else:
        return Result(value=input)


def make_use_thread(f: Callable[[T], U]):
    from .use_thread import use_thread

    def use_result(input: MaybeResult[T]) -> Result[U]:
        input_result = ensure_result(input)

        def in_thread(cancel: threading.Event):
            if input_result.value:
                return f(input_result.value)

        return use_thread(in_thread, dependencies=[input_result.value])

    return use_result


@make_use_thread
def use_json_load(value: bytes):
    return json.loads(value)


def use_json(path):
    return use_fetch(path) | use_json_load


def use_file_content(path, watch=False) -> FileContentResult[bytes]:
    counter, retry = use_retry()

    def read_file(*ignore):
        try:
            with open(path, "rb") as f:
                return f.read()
        except Exception as e:
            return e

    result = None
    try:
        mtime = os.path.getmtime(path)
    except Exception:
        mtime = None

    content = widget.use_memo(read_file, dependencies=[path, mtime, counter])
    if result is not None:
        return result
    if isinstance(content, Exception):
        return FileContentResult[bytes](error=content, _retry=retry)
    else:
        return FileContentResult[bytes](value=content, _retry=retry)


def use_force_update() -> Callable[[], None]:
    """Returns a callable that can be used to force an update of a component.

    This is used when external state has change, and we need to re-render out component.
    """
    _counter, set_counter = widget.use_state(0, "force update counter")

    def updater():
        set_counter(lambda count: count + 1)

    return updater


def use_uuid4(dependencies=[]) -> str:
    """Generate a unique string using the uuid4 algorithm. Will only change when the dependencies change."""

    def make_uuid(*_ignore):
        return str(uuid.uuid4())

    return widget.use_memo(make_uuid, dependencies)


def use_unique_key(key: str = None, prefix: str = "", dependencies=[]) -> str:
    """Generate a unique string, or use key when not None. Dependencies are forwarded to `use_uuid4`."""
    uuid = use_uuid4(dependencies=dependencies)
    return prefix + (key or uuid)


def use_state_or_update(
    initial_or_updated: T, key: str = None, eq: Callable[[Any, Any], bool] = None
) -> Tuple[T, Callable[[Union[T, Callable[[T], T]]], None]]:
    """This is useful for situations where a prop can change from a parent
    component, which should be respected, and otherwise the internal
    state should be kept.
    """
    value, set_value = widget.use_state(initial_or_updated, key=key, eq=eq)

    def possibly_update():
        nonlocal value
        # only gets called when initial_or_updated changes
        set_value(initial_or_updated)
        # this make sure the return value gets updated directly
        value = initial_or_updated

    widget.use_memo(possibly_update, [initial_or_updated])
    return value, set_value


def use_previous(value: T, condition=True) -> T:
    ref = widget.use_ref(value)

    def assign():
        if condition:
            ref.current = value

    widget.use_effect(assign, [value])
    return ref.current
