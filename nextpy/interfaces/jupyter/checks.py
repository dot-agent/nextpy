import json
import logging
import os
import subprocess
import sys
import warnings
from pathlib import Path
from typing import Optional

import IPython.display
from IPython.core.interactiveshell import InteractiveShell
from IPython.display import display

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.util import get_solara_home

HERE = Path(__file__).parent
logger = logging.getLogger(__name__)

jupyter_checked_path = get_solara_home() / ".jupyter_checked"
solara_checked_path = get_solara_home() / ".solara_checked"
# solara_version = widget.__version__


def _should_perform_check(path: Path):
    if path.exists():
        return False
    try:
        home = get_solara_home()
        if not home.exists():
            home.mkdir(parents=True, exist_ok=True)
        # try writing, if we cannot, we will not check
        if not path.exists():
            path.write_text("")
            path.unlink()
    except OSError:
        return False
    return True


def should_perform_jupyter_check():
    if "PYTEST_CURRENT_TEST" in os.environ:
        return False
    return _should_perform_check(jupyter_checked_path)


def should_perform_solara_check():
    if "PYTEST_CURRENT_TEST" in os.environ:
        return False
    import nextpy.interfaces.jupyter.server.settings

    if widget.server.settings.main.mode == "production":
        return False
    return _should_perform_check(solara_checked_path)


# @widget.component
# def JupyterCheck():
#     # We do 2 calls home:
#     #  * 1 from pure js (should always work)
#     #  * 1 from a widget (might not work)
#     # This way we can see how many installations actually fail
#     # Note that we only do this once, we touch ~/.widget/.jupyter_checked
#     # to avoid doing it multiple times
#     def inject_pure_js_check():
#         # do this as an effect, otherwise we will use the display
#         # that gets dispatched to widget, which will not come through
#         # if the widgets do not work
#         IPython.display.display(
#             IPython.display.Javascript(
#                 data=f"""
#                 const prevIframe = document.getElementById("widget-jupyter-check");
#                 if(prevIframe)
#                     prevIframe.remove();
#                 const iframe = document.createElement('iframe')
#                 iframe.setAttribute("src", "https://widget.dev/static/public/success.html?check=purejs&version={1}");
#                 iframe.style.width = "0px";
#                 iframe.style.height = "0px";
#                 iframe.style.display = "none";
#                 iframe.id = "widget-jupyter-check";
#                 document.body.appendChild(iframe);
#                 """
#             )
#         )

#     # this should always get through, even if widgets do not work
#     widget.use_effect(inject_pure_js_check, [])

#     def flag_jupyter_checked():
#         try:
#             jupyter_checked_path.write_text("")
#         except OSError:
#             pass

#     widget.use_effect(flag_jupyter_checked, [])
#     # this iframe should only get through if the widget installation succeeded
#     return widget.v.Html(
#         tag="iframe",
#         attributes={"src": f"https://widget.dev/static/public/success.html?check=widget&version={1}", "width": "0px", "height": "0px"},
#         style_="display: none;",
#     )


@widget.component
def SolaraCheck():
    def flag_solara_checked():
        try:
            solara_checked_path.write_text("")
        except OSError:
            pass

    widget.use_effect(flag_solara_checked, [])
    return widget.v.Html(
        tag="iframe",
        attributes={
            "src": f"https://widget.dev/static/public/success.html?system=widget&check=widget&version={solara_version}",
            "width": "0px",
            "height": "0px",
        },
        style_="display: none;",
    )


def getcmdline(pid):
    # for linux
    if sys.platform == "linux":
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            return f.read().split(b"\00")[0].decode("utf-8")
    elif sys.platform == "darwin":
        return subprocess.check_output(["ps", "-o", "command=", "-p", str(pid)]).split(b"\n")[0].split(b" ")[0].decode("utf-8")
    elif sys.platform == "win32":
        return subprocess.check_output(["wmic", "process", "get", "commandline", "/format:list"]).split(b"\n")[0].split(b" ")[0].decode("utf-8")
    else:
        raise ValueError(f"Unsupported platform: {sys.platform}")


def get_server_python_executable(silent: bool = False):
    servers = []
    try:
        from jupyter_server import serverapp

        servers += list(serverapp.list_running_servers())
    except ImportError:
        pass
    try:
        from notebook import notebookapp

        servers += list(notebookapp.list_running_servers())
    except ImportError:
        pass

    pythons = [getcmdline(server["pid"]) for server in servers]
    if len(pythons) == 0:
        python = sys.executable
        if not silent:
            warnings.warn("Could not find servers, we are assuming the server is running under Python executable: %s" % python)
    elif len(pythons) > 1:
        info = "\n\t".join(pythons)
        if sys.executable in pythons:
            python = sys.executable
        else:
            python = pythons[0]
            if not silent:
                warnings.warn("Found multiple find servers:\n%s\n" "We are assuming the server is running under Python executable: %s" % (info, python))
    else:
        python = pythons[0]
    return python


libraries_minimal = [
    {"python": "ipyvuetify", "classic": "jupyter-vuetify/extension", "lab": "jupyter-vuetify"},
    {"python": "ipyvue", "classic": "jupyter-vue/extension", "lab": "jupyter-vue"},
]

libraries_extra = [
    {"python": "bqplot", "classic": "bqplot/extension", "lab": "bqplot"},
    {"python": "ipyvolume", "classic": "ipyvolume/extension", "lab": "ipyvolume"},
    {"python": "ipywebrtc", "classic": "jupyter-webrtc", "lab": "jupyter-webrtc"},
    {"python": "ipyleaflet", "classic": "ipyleaflet/extension", "lab": "ipyleaflet"},
]


def check_jupyter(
    server_python: Optional[str] = None,
    silent: bool = False,
    libraries: list = libraries_minimal,
    libraries_extra: list = libraries_extra,
    force: bool = False,
    extra: bool = False,
):
    if widget._using_solara_server():
        # for the server we don't need to do this check
        return
    if not InteractiveShell.initialized():
        # also, in a normal python repr, we don't want to display anything
        return
    try:
        python_executable = server_python or get_server_python_executable(silent)
        if Path(python_executable).resolve() != Path(sys.executable).resolve() or force:
            libraries_json = json.dumps(libraries + (libraries_extra if extra else []))
            display(
                IPython.display.Javascript(
                    data="""
                    window.jupyter_python_executable = %r;
                    window.jupyter_widget_checks_silent = %s;
                    window.jupyter_widget_checks_libraries = %s;
                    """
                    % (python_executable, str(silent).lower(), libraries_json)
                )
            )
            display(IPython.display.html(filename=str(HERE / "checks.html")))
        else:
            if not silent:
                display(
                    IPython.display.html(
                        data="<div>Jupyter server is running under the same Python executable as your kernel, no need to check 👍."
                        "<br> <i>Run widget.check_jupyter(force=True) to force checking.</i></div>"
                    )
                )
    except Exception:
        logger.exception("Could not check jupyter-widgets extensions.")


check_jupyter(silent=True)
