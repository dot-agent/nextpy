import abc
import logging
from typing import Callable, List, Optional, Tuple, Union, cast

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter import _using_solara_server

logger = logging.getLogger("widget.router")


class _LocationBase(abc.ABC):
    @property
    def pathname(self):
        pass

    @pathname.setter
    # mypy does not accept this
    # @abc.abstractmethod
    def pathname(self):
        pass


class _Location(_LocationBase):
    def __init__(self, pathname, setter: Callable[[str], None]) -> None:
        self._pathname = pathname
        self.setter = setter

    @property
    def pathname(self):
        return self._pathname

    @pathname.setter
    def pathname(self, value):
        # import pdb

        # pdb.set_trace()
        self._pathname = value
        self.setter(self._pathname)


class Router:
    search: Optional[str]

    def __init__(self, path: str, routes: List[widget.Route], set_path: Callable[[str], None] = None):
        # see https://developer.mozilla.org/en-US/docs/Web/API/Location for anatomy/nomenclature
        if "?" in path:
            self.path, self.search = path.split("?", 1)
        else:
            self.path = path
            self.search = None
        del path
        self.set_path = set_path
        self.parts = (self.path or "").strip("/").split("/")
        self.routes = routes
        self.root_path = ""
        if _using_solara_server():
            import nextpy.interfaces.jupyter.server.settings

            self.root_path = widget.server.settings.main.root_path or ""
        # each route in this list corresponds to a part in self.parts
        self.path_routes: List["widget.Route"] = []
        self.path_routes_siblings: List[List["widget.Route"]] = []  # siblings including itself
        # routes = routes.copy()
        route = None
        for part in self.parts:
            for route in routes:
                if (route.path == part) or (route.path == "/" and not part):
                    self.path_routes.append(route)
                    self.path_routes_siblings.append(routes)
                    routes = route.children
                    break
        if len(self.parts) == len(self.path_routes):
            # e.g. '/foo/bar' -> ['foo', 'bar'] and bar has a default route
            # but if '' -> [''] we should not
            route = self.path_routes[-1]
            if route:
                default_routes = [k for k in route.children if k.path == "/"]
                if self.parts and self.parts[0] and default_routes:
                    self.path_routes.append(default_routes[0])
                    self.path_routes_siblings.append(route.children)

        assert len(self.path_routes) == len(self.path_routes_siblings)
        self.possible_match = (len(self.path_routes[-1].children) == 0) if self.path_routes else False

    def push(self, path: str):
        assert self.set_path is not None
        self.set_path(path)


router_context = widget.create_context(Router("", []))
_location_context = widget.create_context(cast(_LocationBase, _Location("", lambda x: None)))

route_level_context = widget.create_context(0)


def use_route_level():
    route_level = widget.use_context(route_level_context)
    return route_level


def use_router() -> Router:
    """Returns the current router object.

    See also [Understanding Routing](/docs/understanding/routing).

    `use_router` returns the current router object. This is useful to build custom routing.

    the router object contains the following properties/methods:

     * `path` - the current pathname (e.g. `/fruit/banana`)
     * `parts` - the current pathname split into parts (e.g. `['fruit', 'banana']`)
     * `search` - the current search string (e.g. `color=yellow`)
     * `push(path: str)` - navigate to path (e.g. `router.push('/fruit/banana')`)

    ## Typical usage:

    ```python
    import nextpy.interfaces.jupyter


    @widget.component
    def Page():
        router = widget.use_router()

        def redirect():
            router.push(f"/api/use_route")

        widget.button("Navigate using an event", on_click=redirect)
    ```

    """
    return widget.use_context(router_context)


def use_route(
    level=0,
    peek=False,
) -> Tuple[Optional[widget.Route], List[widget.Route]]:
    """Returns (if found) the current route that matches the pathname, or None

    See also [Understanding Routing](/docs/understanding/routing).

    `use_route` returns (if found) the current route that matches the pathname, or None. It also returns all resolved routes of that level
    (i.e. all siblings and itself). This return tuple is useful to build custom navigation (e.g. using tabs or buttons).


    Routing starts with declaring a set of `routes` in your app (widget picks up the `routes` variable if it exists,
    and it should be in the same namespace as `Page`).
    In the demo below, we declared the following routes.

    ```python
    routes = [
        widget.Route(path="/"),
        widget.Route(
            path="fruit",
            component=Fruit,
            children=[
                widget.Route(path="/"),
                widget.Route(path="kiwi"),
                widget.Route(path="banana"),
                widget.Route(path="apple"),
            ],
        ),
    ]
    ```

    Note that all routes are relative, since a component does not know if it is embedded into a larger application, which may also do routing.
    Therefore you should never use the `route.path` for navigation since the route object has no knowledge of the full url
    (e.g. `/api/use_route/fruit/banana`) but only knows its small piece of the pathname (e.g. `banana`)

    Use [`resolve_path`](/api/resolve_path) to request the full url for navigation, or simply use the `Link` component that can do this for us.

    If the current route has children, any child component that calls `use_route` will return the matched route and its siblings of our children.


    ## Arguments

    * `level`: the level of the route to return. 0 is the current route, -1 is the parent route, 1 the child route, etc.
    * `peek`: if True, the route level is not incremented. This is useful to peek at the next route level without changing the current route level.
    """

    router = widget.use_context(router_context)
    route_level = widget.use_context(route_level_context)
    if not peek:
        route_level_context.provide(route_level + 1)
    route_level += level
    if route_level < len(router.path_routes):
        return router.path_routes[route_level], router.path_routes_siblings[route_level]
    else:
        return None, []


def find_route(path: str) -> Optional[widget.Route]:
    router = widget.get_context(router_context)
    route_level = min(widget.get_context(route_level_context), len(router.path_routes_siblings) - 1)
    for route in router.path_routes_siblings[route_level]:
        if path.startswith(route.path) or (not path and route.path == "/"):
            return route
    return None


def use_pathname():
    location_proxy = widget.use_context(_location_context)

    def setter(value):
        location_proxy.pathname = value

    return location_proxy.pathname, setter


def resolve_path(path_or_route: Union[str, widget.Route], level=0) -> str:
    """Resolve a relative path or a route to an absolute path.

    If the path is a string and starts with a `/'`, it is returned as is.


    ## Typical usage:

    ```python
    ...
    route_current, routes_current_level = widget.routes()
    # route_current.path == "banana"
    path = widget.resolve_path(route_current)
    # path == "/fruit/banana"
    path_same = widget.resolve_path("banana")
    # path_same == path == "/fruit/banana"
    ...
    ```

    ## Arguments

     * path_or_route: a path string or a [`widget.Route`](/api/route) object to resolve.

    ## See also

     * [Multipage](/docs/howto/multipage).
     * [Understanding Routing](/docs/understanding/routing).


    """
    router = widget.get_context(router_context)
    if isinstance(path_or_route, str):
        path = path_or_route
        if path.startswith("/"):
            return path
        route_level = widget.get_context(route_level_context) + level
        parts = [*router.parts[:route_level], path]
        path = "/" + "/".join(parts)
        if path.startswith("//"):
            path = path[1:]
        return path
    elif isinstance(path_or_route, widget.Route):
        route: widget.Route = path_or_route
        path = _resolve_path("/", route, router.routes)
        if path.startswith("//"):
            path = path[1:]
        return path


def _resolve_path(prefix: str, findroute: widget.Route, routes: List[widget.Route]):
    for route in routes:
        path = (prefix + "/" + route.path) if route.path != "/" else prefix
        if findroute is route:
            return path
        possible_path = _resolve_path(path, findroute=findroute, routes=route.children)
        if possible_path is not None:
            return possible_path
