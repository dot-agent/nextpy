import dataclasses
from enum import Enum
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar, Union

import reacton
from typing_extensions import Literal, TypedDict

T = TypeVar("T")
U = TypeVar("U")


@dataclasses.dataclass(frozen=True)
class Action:
    name: str
    icon: Optional[str] = None
    on_click: Optional[Callable] = None


@dataclasses.dataclass(frozen=True)
class columnAction(Action):
    on_click: Optional[Callable[[str], None]] = None


@dataclasses.dataclass(frozen=True)
class CellAction(Action):
    on_click: Optional[Callable[[str, int], None]] = None


def _fallback_retry():
    raise RuntimeError("Should not happen")


class ResultState(Enum):
    INITIAL = 1
    STARTING = 2
    WAITING = 3
    RUNNING = 4
    ERROR = 5
    FINISHED = 6
    CANCELLED = 7


@dataclasses.dataclass(frozen=True)
class Result(Generic[T]):
    value: Optional[T] = None
    error: Optional[Exception] = None
    state: ResultState = ResultState.INITIAL
    progress: Optional[float] = None

    def retry(self):
        # mypy does not like members that are callable
        # gets confused about self argument.
        # we wrap it to avoid hitting this error in user
        # code
        self._retry()  # type: ignore

    # can we avoid storing these into the dataclass?
    _retry: Callable[[], Any] = dataclasses.field(compare=False, default=lambda: None)
    cancel: Callable[[], Any] = dataclasses.field(compare=False, default=lambda: None)

    def __or__(self, next: Callable[["Result[T]"], "Result[U]"]):
        return next(self)


@dataclasses.dataclass(frozen=True)
class FileContentResult(Result[T]):
    @property
    def exists(self):
        return not isinstance(self.error, FileNotFoundError)


class AggregationCount(TypedDict):
    type: Literal["count"]


class AggregationSum(TypedDict):
    type: Literal["sum"]


JsonType = Union[None, int, str, bool, List[Any], Dict[str, Any]]

Aggregation = Union[AggregationCount, AggregationSum]


class PivotTableData(TypedDict):
    x: List[str]
    y: List[str]
    agg: str
    values: List[List[JsonType]]
    values_x: List[str]
    values_y: List[str]
    headers_x: List[List[str]]
    headers_y: List[List[str]]
    counts_x: int
    counts_y: int
    total: str


@dataclasses.dataclass(frozen=True)
class Route:
    """A route tells Solara which component to render for a given URL. (Not a Solara component!)

    ## Arguments

     * `path` - The path of the route. This is the part of the URL that you see in the browser.
     * `children` - (Optional) A list of child routes. These are routes that are nested under this route.
     * `module` - (Optional) The module that contains the component to render for this route, used for autorouting.
     * `component` - (Optional) The component to render for this route.
     * `layout` - (Optional) The layout to use for this route. If not specified, the default layout will be used.
     * `data` - (Optional) The data to pass to the component for this route, usage is up to the user.
     * `label` - (Optional) The label to use for this route, can be used for labeling tabs or links.

    ## See also

     * [Multipage](/docs/howto/multipage).
     * [Understanding Routing](/docs/understanding/routing).

    """

    path: str
    children: List["Route"] = dataclasses.field(default_factory=list)

    # these are free to use, depending on the implementation
    # see autorouting.py for how Solara uses them
    module: Optional[ModuleType] = None

    # in the autorouting implementation, this is the
    # the same as module.Page (unless we are rendering a markdown)
    component: Union[None, Callable, reacton.core.Component] = None
    layout: Union[None, Callable, reacton.core.Component] = None

    # in the autorouting implementation, this is the
    # path of the markdown file
    data: Any = None

    # Can be used for a title and/or a tab label
    label: Optional[str] = None

    # file corresponding to this route, can be used for
    # checking of content has changed (using mtime)
    file: Optional[Path] = None
