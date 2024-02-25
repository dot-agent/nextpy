import base64
import contextlib
import hashlib
import os
import sys
import threading
from collections import abc
from pathlib import Path
from typing import TYPE_CHECKING, Dict, List, Tuple, Union

if TYPE_CHECKING:
    import numpy as np

import ipyvuetify
import ipywidgets
import reacton

import nextpy.interfaces.jupyter as widget

SOLARA_ALLOW_OTHER_TRACER = os.environ.get("SOLARA_ALLOW_OTHER_TRACER", False) in (True, "True", "true", "1")
ipyvuetify_major_version = int(ipyvuetify.__version__.split(".")[0])
ipywidgets_major = int(ipywidgets.__version__.split(".")[0])


def github_url(file):
    rel_path = os.path.relpath(file, Path(widget.__file__).parent.parent)
    github_url = widget.github_url + f"/blob/{widget.git_branch}/" + rel_path
    return github_url


def github_edit_url(file):
    # e.g. https://github.com/widgetti/widget/edit/master/widget/__init__.py
    rel_path = os.path.relpath(file, Path(widget.__file__).parent.parent)
    github_url = widget.github_url + f"/edit/{widget.git_branch}/" + rel_path
    return github_url


def load_file_as_data_url(file_name, mime):
    with open(file_name, "rb") as f:
        data = f.read()
    return f"data:{mime};base64," + base64.b64encode(data).decode("utf-8")


def isinstanceof(object, spec: str):
    """Check if object is instance of type '<modulename>:<classname>'

    This can avoid a runtime dependency, since we do not need to import `modulename`.

    >>> import numpy as np
    >>> isinstanceof(np.arange(2), "numpy:ndarray")
    True
    """
    module_name, classname = spec.split(":")
    module = sys.modules.get(module_name)
    if module:
        cls = getattr(module, classname)
        return isinstance(object, cls)
    return False


def numpy_to_image(data: "np.ndarray", format="png"):
    import io

    if data.ndim == 3:
        try:
            import PIL.Image
        except ModuleNotFoundError:
            raise ModuleNotFoundError("Pillow is required to convert numpy array to image, use pip install pillow to install it.")
        if data.shape[2] == 3:
            im = PIL.Image.fromarray(data[::], "RGB")
        elif data.shape[2] == 4:
            im = PIL.Image.fromarray(data[::], "RGBA")
        else:
            raise ValueError(f"Expected last dimension to have 3 or 4 dimensions, total shape we got was {data.shape}")
        f = io.BytesIO()
        im.save(f, format)
        return f.getvalue()
    else:
        raise ValueError(f"Expected an image with 3 dimensions (height, width, channel), not {data.shape}")


@contextlib.contextmanager
def cwd(path):
    cwd = os.getcwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(cwd)


def numpy_equals(a, b):
    import numpy as np

    if a is b:
        return True
    if a is None or b is None:
        return False
    if np.all(a == b):
        return True
    return False


def _combine_classes(class_list: List[str]) -> str:
    return " ".join(class_list)


def _flatten_style(style: Union[str, Dict, None] = None) -> str:
    if style is None:
        return ""
    elif isinstance(style, str):
        return style
    elif isinstance(style, dict):
        return ";".join(f"{k}:{v}" for k, v in style.items()) + ";"
    else:
        raise ValueError(f"Expected style to be a string or dict, got {type(style)}")


def import_item(name: str):
    """Import an object by name like widget.cache.LRU"""
    parts = name.rsplit(".", 2)
    if len(parts) == 1:
        return __import__(name)
    else:
        # TODO - fix later
        import nextpy.interfaces.jupyter as widget
        module = __import__(".".join(parts[:-1]), fromlist=[parts[-1]])
        return getattr(module, parts[-1])


def get_solara_home() -> Path:
    """Get widget home directory, defaults to ~/.widget.

    The $SOLARA_HOME environment variable can be set to override this default.

    If $SOLARA_HOME is not defined and ~ cannot be expanded, the current working directory + ".widget" is used.
    """
    os_home = None
    try:
        os_home = Path.home()
    except Exception:
        pass
    if "SOLARA_HOME" in os.environ:
        return Path(os.environ["SOLARA_HOME"])
    elif os_home:
        return os_home / ".widget"
    else:
        return Path(os.getcwd()) / ".widget"


def parse_size(size: str) -> int:
    """Given a human readable size, return the number of bytes.

    Supports GB, MB, KB, and bytes. E.g. 10GB, 500MB, 1KB, 1000

    Commas and _ are ignored, e.g. 1,000,000 is the same as 1000000.
    """
    size = size.replace(",", "").replace("_", "").upper()
    if size.endswith("GB"):
        return int(float(size[:-2]) * 1024 * 1024 * 1024)
    elif size.endswith("MB"):
        return int(float(size[:-2]) * 1024 * 1024)
    elif size.endswith("KB"):
        return int(float(size[:-2]) * 1024)
    elif size.endswith("B"):
        return int(float(size[:-1]))
    else:
        return int(size)


def nested_get(object, dotted_name: str, default=None):
    names = dotted_name.split(".")
    for name in names:
        if isinstance(object, abc.Mapping):
            if name == names[-1]:
                object = object.get(name, default)
            else:
                object = object.get(name)
        else:
            if name == names[-1]:
                object = getattr(object, name, default)
            else:
                object = getattr(object, name)
    return object


# inherit from BaseException so less change of being caught
# in an except
class CancelledError(BaseException):
    pass


# not available in python 3.6
class nullcontext(contextlib.AbstractContextManager):
    def __init__(self, enter_result=None):
        self.enter_result = enter_result

    def __enter__(self):
        return self.enter_result

    def __exit__(self, *excinfo):
        pass


@contextlib.contextmanager
def cancel_guard(cancelled: threading.Event):
    def tracefunc(frame, event, arg):
        # this gets called at least for every line executed
        if cancelled.is_set():
            rc = reacton.core.get_render_context(required=False)
            # we do not want to cancel the rendering cycle
            if rc is None or not rc._is_rendering:
                # this will bubble up
                raise CancelledError()
        if prev and SOLARA_ALLOW_OTHER_TRACER:
            prev(frame, event, arg)
        # keep tracing:
        return tracefunc

    # see https://docs.python.org/3/library/sys.html#sys.settrace
    # it is for the calling thread only
    # not every Python implementation has it
    prev = None
    if hasattr(sys, "gettrace"):
        prev = sys.gettrace()
    if hasattr(sys, "settrace"):
        sys.settrace(tracefunc)
    try:
        yield
    finally:
        if hasattr(sys, "settrace"):
            sys.settrace(prev)


def parse_timedelta(size: str) -> float:
    """Turn a human readable time delta into seconds.
    Supports days(d), hours (h), minutes (m) and seconds (s).
    If not unit is specified, seconds is assumed.
    >>> parse_timedelta("1d")
    86400
    >>> parse_timedelta("1h")
    3600
    >>> parse_timedelta("30m")
    1800
    >>> parse_timedelta("10s")
    10
    >>> parse_timedelta("10")
    10
    """
    if size.endswith("d"):
        return float(size[:-1]) * 24 * 60 * 60
    elif size.endswith("h"):
        return float(size[:-1]) * 60 * 60
    elif size.endswith("m"):
        return float(size[:-1]) * 60
    elif size.endswith("s"):
        return float(size[:-1])
    else:
        return float(size)


def get_file_hash(path: Path, algorithm="md5") -> Tuple[bytes, str]:
    """Compute the hash of a file. Note that we also return the file content as bytes."""
    data = path.read_bytes()
    if sys.version_info[:2] < (3, 9):
        # usedforsecurity is only available in Python 3.9+
        h = hashlib.new(algorithm)
    else:
        h = hashlib.new(algorithm, usedforsecurity=False)  # type: ignore
    h.update(data)
    return data, h.hexdigest()
