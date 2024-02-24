import os

import ipyvuetify as v
import ipywidgets
import traitlets

__all__ = [
    "VegaLite",
    "Navigator",
    "GridLayout",
    "html",
    "watch",
]


class VegaLite(v.VuetifyTemplate):
    template_file = os.path.realpath(os.path.join(os.path.dirname(__file__), "vue/vegalite.vue"))
    spec = traitlets.Dict().tag(sync=True)
    listen_to_click = traitlets.Bool(False).tag(sync=True)
    listen_to_hover = traitlets.Bool(False).tag(sync=True)
    on_click = traitlets.traitlets.Callable(None, allow_none=True)
    on_hover = traitlets.traitlets.Callable(None, allow_none=True)

    def vue_altair_click(self, *args):
        if self.on_click:
            self.on_click(*args)

    def vue_altair_hover(self, *args):
        if self.on_hover:
            self.on_hover(*args)


class Navigator(v.VuetifyTemplate):
    template_file = os.path.realpath(os.path.join(os.path.dirname(__file__), "vue/navigator.vue"))
    location = traitlets.Unicode(None, allow_none=True).tag(sync=True)


class GridLayout(v.VuetifyTemplate):
    template_file = os.path.join(os.path.dirname(__file__), "vue/gridlayout.vue")
    gridlayout_loaded = traitlets.Bool(False).tag(sync=True)
    items = traitlets.Union([traitlets.List(), traitlets.Dict()], default_value=[]).tag(sync=True, **ipywidgets.widget_serialization)
    grid_layout = traitlets.List(default_value=[]).tag(sync=True)
    draggable = traitlets.CBool(True).tag(sync=True)
    resizable = traitlets.CBool(True).tag(sync=True)


class html(v.VuetifyTemplate):
    template_file = os.path.realpath(os.path.join(os.path.dirname(__file__), "vue/html.vue"))
    tag = traitlets.Unicode("div").tag(sync=True)
    attributes = traitlets.Dict().tag(sync=True)
    unsafe_innerHTML = traitlets.Unicode(None, allow_none=True).tag(sync=True)


def watch():
    import ipyvue

    ipyvue.watch(os.path.realpath(os.path.dirname(__file__) + "/vue"))
