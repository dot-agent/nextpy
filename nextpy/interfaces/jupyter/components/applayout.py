from typing import Callable, Dict, List, Optional, Tuple, Union, cast

import reacton
import reacton.core
import reacton.ipyvuetify as v
import reacton.utils
from reacton.core import Element

import nextpy.interfaces.jupyter as widget


from .typography import title_file as t


@widget.component
def AppIcon(open=False, on_click=None, **kwargs):
    def click(*ignore):
        on_click()

    icon = v.AppBarNavIcon(**kwargs)
    v.use_event(icon, "click", click)
    return icon


should_use_embed = widget.create_context(False)
PortalElements = Dict[str, List[Tuple[int, Element]]]


def _set_sidebar_default(updater: Callable[[PortalElements], PortalElements]):
    pass


class ElementPortal:
    def __init__(self):
        self.context = widget.create_context(_set_sidebar_default)

    # TODO: can we generalize the use of 'portals' ? (i.e. transporting elements from one place to another)
    def use_portal(self) -> List[Element]:
        portal_elements, set_portal_elements = widget.use_state(cast(PortalElements, {}))
        self.context.provide(set_portal_elements)  # type: ignore

        portal_elements_flat: List[Tuple[int, Element]] = []
        for uuid, value in portal_elements.items():
            portal_elements_flat.extend(value)
        portal_elements_flat.sort(key=lambda x: x[0])
        return [e[1] for e in portal_elements_flat]

    def use_portal_add(self, children: List[Element], offset: int):
        key = widget.use_unique_key(prefix="portal-")
        set_portal_elements = widget.use_context(self.context)
        values: List[Tuple[int, Element]] = []
        for i, child in enumerate(children):
            values.append((offset + i, child))

        # updates we do when children/offset changes
        def add():
            # we use the update function method, to avoid stale data
            def update_dict(portal_elements):
                portal_elements_updated = portal_elements.copy()
                portal_elements_updated[key] = values
                return portal_elements_updated

            set_portal_elements(update_dict)

        widget.use_effect(add, [values])

        # cleanup we only need to do after component removal
        def add_cleanup():
            def cleanup():
                def without(portal_elements):
                    portal_elements_restored = portal_elements.copy()
                    portal_elements_restored.pop(key, None)
                    return portal_elements_restored

                set_portal_elements(without)

            return cleanup

        widget.use_effect(add_cleanup, [])


sidebar_portal = ElementPortal()
appbar_portal = ElementPortal()
apptitle_portal = ElementPortal()


@widget.component
def AppBar(children=[]):
    """Puts its children in the app bar of the AppLayout (or any layout that supports it).

    This component does not need to be a direct child of the AppLayout, it can be at any level in your component tree.

    If a [Tabs](/api/tabs) component is used as direct child of the app bar, it will be shown under the app bar.

    ## Example showing an app bar
    ```widget
    import widget

    @widget.component
    def Page():
        logged_in, set_logged_in = widget.use_state(False)
        def toggle_login():
            set_logged_in(not logged_in)

        with widget.AppBar():
            icon_name = "mdi-logout" if logged_in else "mdi-login"
            widget.button(icon_name=icon_name , on_click=toggle_login, icon=True)
        with widget.column():
            if logged_in:
                widget.Info("You are logged in")
            else:
                widget.Error("You are logged out")
    ```
    """
    # TODO: generalize this, this is also used in title
    level = 0
    rc = reacton.core.get_render_context()
    context = rc.context
    while context and context.parent:
        level += 1
        context = context.parent
    offset = 2**level
    appbar_portal.use_portal_add(children, offset)

    return widget.div(style="display; none")


@widget.component
def AppBarTitle(children=[]):
    """Puts its children in the title section of the AppBar (or any layout that supports it).

    This component does not need to be a direct child of the AppBar, it can be at any level in your component tree.

    ## Example

    ```widget
    import widget

    @widget.component
    def Page():
        with widget.AppBarTitle():
            widget.text("Hi there")
            widget.button("Click me", outlined=True, classes=["mx-2"])
    ```
    """
    level = 0
    rc = reacton.core.get_render_context()
    context = rc.context
    while context and context.parent:
        level += 1
        context = context.parent
    offset = 2**level
    apptitle_portal.use_portal_add(children, offset)

    return widget.div(style="display; none")


@widget.component
def Sidebar(children=[]):
    """Puts its children in the sidebar of the AppLayout (or any layout that supports it).
    This component does not need to be a direct child of the AppLayout, it can be at any level in your component tree.

    On the widget.dev website and in the Jupyter notebook, the sidebar is shown in a dialog instead (embedded mode)

    ## Example showing a sidebar (embedded mode)
    ```widget
    import widget

    @widget.component
    def Page():
        with widget.column() as main:
            with widget.Sidebar():
                widget.Markdown("## I am in the sidebar")
                widget.SliderInt(label="Ideal for placing controls")
            widget.Info("I'm in the main content area, put your main content here")
        return main
    ```


    """
    # TODO: generalize this, this is also used in title
    level = 0
    rc = reacton.core.get_render_context()
    context = rc.context
    while context and context.parent:
        level += 1
        context = context.parent
    offset = 2**level
    sidebar_portal.use_portal_add(children, offset)

    return widget.div(style="display; none")


@widget.component
def AppLayout(
    children=[],
    sidebar_open=True,
    title=None,
    navigation=True,
    toolbar_dark=True,
    color: Optional[str] = "primary",
    classes: List[str] = [],
    style: Optional[Union[str, Dict[str, str]]] = None,
):
    """The default layout for Solara apps. It consists of an toolbar bar, a sidebar and a main content area.

     * The title of the app is set using the [Title](/api/title) component.
     * The sidebar content is set using the [Sidebar](/api/sidebar) component.
     * The content is set by the `Page` component provided by the user.

    This component is usually not used directly, but rather through via the [Layout system](/docs/howto/layout).

    The sidebar is only added when the AppLayout has more than one child.

    ```python
    with AppLayout(title="My App"):
        with v.Card():
            ...  # sidebar content
        with v.Card():
            ...  # main content
    ```

    # Arguments

     * `children`: The children of the AppLayout. The first child is used as the sidebar content, the rest as the main content.
     * `sidebar_open`: Whether the sidebar is open or not.
     * `title`: The title of the app shown in the app bar, can also be set using the [Title](/api/title) component.
     * `toolbar_dark`: Whether the toolbar should be dark or not.
     * `navigation`: Whether the navigation tabs based on routing should be shown.
     * `color`: The color of the toolbar.
     * `classes`: List of CSS classes to apply to the direct parent of the childred.
     * `style`: CSS style to apply to the direct parent of the children. If style is None we use a default style of "height: 100%; overflow: auto;"
        and add 12px of padding when the sidebar of titlebar is visible. This will make sure your app gets scrollbars when need.
    """
    route, routes = widget.use_route()
    paths = [widget.resolve_path(r, level=0) for r in routes]
    location = widget.use_context(widget.routing._location_context)
    embedded_mode = widget.use_context(should_use_embed)
    fullscreen, set_fullscreen = widget.use_state(False)
    # we cannot nest AppLayouts, so we can use the context to set the embedded mode
    should_use_embed.provide(True)
    index = routes.index(route) if route else None

    sidebar_open, set_sidebar_open = widget.use_state_or_update(sidebar_open)
    # remove the appbar from the children
    children_without_portal_sources = [c for c in children if c.component != AppBar]
    use_drawer = len(children_without_portal_sources) > 1
    children_content = children
    children_sidebar = []
    if use_drawer:
        child_sidebar = children_without_portal_sources.pop(0)
        children_sidebar = [child_sidebar]
        children_content = [c for c in children if c is not child_sidebar]
    children_sidebar = children_sidebar + sidebar_portal.use_portal()
    children_appbar = appbar_portal.use_portal()
    if children_sidebar:
        use_drawer = True
    title = t.use_title_get() or title
    children_appbartitle = apptitle_portal.use_portal()
    show_app_bar = (title and (len(routes) > 1 and navigation)) or children_appbar or use_drawer or children_appbartitle

    if style is None:
        style = {"height": "100%", "overflow": "auto"}
        # if style is None, we choose a default style based on whether we are seeing the appbar, etc
        if show_app_bar or children_sidebar or len(children) != 1:
            style["padding"] = "12px"

    def set_path(index):
        path = paths[index]
        location.pathname = path

    v_slots = []

    tabs = None
    for child_appbar in children_appbar.copy():
        if child_appbar.component == widget.lab.Tabs:
            if tabs is not None:
                raise ValueError("Only one Tabs component is allowed in the AppBar")
            tabs = child_appbar
            children_appbar.remove(tabs)

    if (tabs is None) and routes and navigation and (len(routes) > 1):
        with widget.lab.Tabs(value=index, on_value=set_path, align="center") as tabs:
            for route in routes:
                name = route.path if route.path != "/" else "Home"
                widget.lab.Tab(name)
        # with v.Tabs(v_model=index, on_v_model=set_path, centered=True) as tabs:
        #     for route in routes:
        #         name = route.path if route.path != "/" else "Home"
        #         v.Tab(children=[name])
    if tabs is not None:
        v_slots = [{"name": "extension", "children": tabs}]
    if embedded_mode and not fullscreen:
        # this version doesn't need to run fullscreen
        # also ideal in widget notebooks
        with v.Html(tag="div") as main:
            if show_app_bar or use_drawer:
                with v.AppBar(color=color, dark=toolbar_dark, v_slots=v_slots):
                    if use_drawer:
                        icon = AppIcon(sidebar_open, on_click=lambda: set_sidebar_open(not sidebar_open), v_on="x.on")
                        with v.Menu(
                            offset_y=True,
                            nudge_left="50px",
                            left=True,
                            v_slots=[{"name": "activator", "variable": "x", "children": [icon]}],
                            close_on_content_click=False,
                        ):
                            pass
                            v.Html(tag="div", children=children_sidebar, style_="background-color: white; padding: 12px; min-width: 400px")
                    if title or children_appbartitle:
                        v.ToolbarTitle(children=children_appbartitle or [title])
                    v.Spacer()
                    for child in children_appbar:
                        widget.display(child)
                    widget.button(icon_name="mdi-fullscreen", on_click=lambda: set_fullscreen(True), icon=True, dark=False)
            with v.Row(no_gutters=False, class_="widget-content-main"):
                v.Col(cols=12, children=children_content)
    else:
        # this limits the height of the app to the height of the screen
        # and further down we use overflow: auto to add scrollbars to the main content
        # the navigation drawer adds it own scrollbars
        # NOTE: while developing this we added overflow: hidden, but this does not seem
        # to be necessary anymore
        with v.Html(tag="div", style_="height: 100vh") as main:
            with widget.hstack():
                if use_drawer:
                    with v.NavigationDrawer(
                        width="min-content",
                        v_model=sidebar_open,
                        on_v_model=set_sidebar_open,
                        style_="min-width: 400px; max-width: 600px",
                        clipped=True,
                        app=True,
                        # disable_resize_watcher=True,
                        disable_route_watcher=True,
                        mobile_break_point="960",
                        class_="widget-content-main",
                    ):
                        if not show_app_bar:
                            AppIcon(sidebar_open, on_click=lambda: set_sidebar_open(not sidebar_open))
                        v.Html(tag="div", children=children_sidebar, style_="padding: 12px;").meta(ref="sidebar-content")
            if show_app_bar:
                # if hide_on_scroll is True, and we have a little bit of scrolling, vuetify seems to act strangely
                # when scrolling (on @mariobuikhuizen/vuetify v2.2.26-rc.0
                with v.AppBar(color=color, dark=True, app=True, clipped_left=True, hide_on_scroll=False, v_slots=v_slots).key("app-layout-appbar"):
                    if use_drawer:
                        AppIcon(sidebar_open, on_click=lambda: set_sidebar_open(not sidebar_open))
                    if title or children_appbartitle:
                        v.ToolbarTitle(children=children_appbartitle or [title])
                    v.Spacer()
                    for i, child in enumerate(children_appbar):
                        # if the user already provided a key, don't override it
                        if child._key is None:
                            widget.display(child.key(f"app-layout-appbar-user-child-{i}"))
                        else:
                            widget.display(child)
                    if fullscreen:
                        widget.button(icon_name="mdi-fullscreen-exit", on_click=lambda: set_fullscreen(False), icon=True, dark=False)
            # in vue2 is was v-content, in vue3 it is v-main
            MainComponent = v.Main if widget.util.ipyvuetify_major_version == 3 else v.Content  # type: ignore
            with MainComponent(class_="widget-content-main", style_="height: 100%;").key("app-layout-content"):
                # make sure the scrollbar does no go under the appbar by adding overflow: auto
                # to a child of content, because content has padding-top: 64px (set by vuetify)
                # the padding: 12px is needed for backward compatibility with the previously used
                # v.Col which has this by default. If we do not use this, a widget.column will
                # use a margin: -12px which will make a horizontal scrollbar appear
                widget.div(style=style, classes=classes, children=children_content)
        if fullscreen:
            with v.Dialog(v_model=True, children=[], fullscreen=True, hide_overlay=True, persistent=True, no_click_animation=True) as dialog:
                v.Sheet(class_="overflow-y-auto overflow-x-auto", children=[main])
                pass
            return dialog
    return main


@widget.component
def _AppLayoutEmbed(children=[], sidebar_open=True, title=None):
    """Forces the embed more for a AppLayout. This is used by default in Jupyter."""
    should_use_embed.provide(True)

    if widget.checks.should_perform_jupyter_check():
        print('111111111111111111',children)
        # children = [widget.column(children=children + [widget.checks.JupyterCheck()])]
        children = [widget.column(children=children)]

    def once():
        # import widget.server.telemetry
        import solara.server.telemetry

        # widget.server.telemetry.jupyter_start()
        solara.server.telemetry.jupyter_start()

    widget.use_effect(once, [])
    return AppLayout(children=children, sidebar_open=sidebar_open, title=title)


reacton.core.jupyter_decorator_components.append(_AppLayoutEmbed)
