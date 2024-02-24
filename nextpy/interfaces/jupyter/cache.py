import hashlib
import inspect
import logging
import sys
from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    MutableMapping,
    Optional,
    TypeVar,
    Union,
    cast,
    overload,
)

import cachetools
import nextpy.interfaces.jupyter as widget
import nextpy.interfaces.jupyter.settings
import nextpy.interfaces.jupyter.util
import typing_extensions
from reacton.utils import equals

logger = logging.getLogger("widget.cache")

# placeholder value for missing keys
_DOES_NOT_EXIST = object()

_global_values_used: Dict[Any, Dict[str, Any]] = {}


T = TypeVar("T")
R = TypeVar("R")
K = TypeVar("K")
V = TypeVar("V")
P = typing_extensions.ParamSpec("P")

Storage = MutableMapping[K, V]


class Memory(cachetools.LRUCache):
    def __init__(self, max_items=widget.settings.cache.memory_max_items):
        super().__init__(maxsize=max_items)


def _default_key(*args, **kwargs):
    kwargs_tuple: Any = ()
    for key, value in kwargs.items():
        kwargs_tuple += (key, value)
    return (args, kwargs_tuple)


class MemoizedFunction(Generic[P, R]):
    def __init__(self, function: Callable[P, R], key: Callable[P, R], storage: Optional[Storage], allow_nonlocals=False):
        self.function = function
        f: Callable = self.function
        if not allow_nonlocals:
            nonlocals = inspect.getclosurevars(f).nonlocals
            if nonlocals:
                raise ValueError(f"Memoized functions cannot depend on nonlocal variables, it now depends on {nonlocals}")
        if sys.version_info[:2] < (3, 9):
            # usedforsecurity is only available in Python 3.9+
            codehash = hashlib.md5(f.__code__.co_code).hexdigest()
        else:
            codehash = hashlib.md5(f.__code__.co_code, usedforsecurity=False).hexdigest()  # type: ignore

        self.function_key = (f.__qualname__, codehash)
        current_globals = dict(inspect.getclosurevars(f).globals)
        _global_values_used.setdefault(self.function_key, current_globals)
        self._check_globals()
        self.key = key
        self._storage = storage
        self.intrusive_cancel = True
        # modifications to these are not thread safe
        # but good enough for an indication
        self.hits = 0
        self.misses = 0

    @property
    def storage(self) -> Storage:
        return self._storage if self._storage is not None else storage

    def _check_globals(self):
        globals = _global_values_used.get(self.function_key)
        current_globals = dict(inspect.getclosurevars(self.function).globals)
        if current_globals is not globals:
            if not equals(current_globals, globals):
                raise ValueError(
                    f"Memoized functions depend on globals variables, but they changed. The first value was {globals}, but now it is {current_globals}"
                )

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        self._check_globals()
        key = (self.function_key, self.key(*args, **kwargs))
        # if .get is atomic, we do not need to lock
        value = cast(R, self.storage.get(key, _DOES_NOT_EXIST))
        if value is _DOES_NOT_EXIST:
            self.misses += 1
            value = self.function(*args, **kwargs)
            self.storage[key] = value
        else:
            self.hits += 1
        return value

    def use_thread(self, *args: P.args, **kwargs: P.kwargs) -> widget.Result[R]:
        """Calls the function in a thread when not in cache, otherwise returns the cached value.

        This is almost similar to a use_thread on the memoized function, except that
        we ensure that if the function return value is already in the cache, we don't
        have to wait for the thread to finish.

        This can cause less flickering in the UI, since it will immediately return a
        'FINISHED' result, instead of a 'RUNNING' result when possible.
        """
        key = (self.function_key, self.key(*args, **kwargs))

        # we assume generating the key is cheap, but a storage.get might not be
        # since it may have to ask the a server, so we wrap it in use_memo
        def get_current():
            return cast(R, self.storage.get(key, _DOES_NOT_EXIST))

        value = widget.use_memo(get_current, dependencies=[key])

        def do_work():
            if value is _DOES_NOT_EXIST:
                self.misses += 1
                self._check_globals()
                new_value = self.function(*args, **kwargs)
                # TODO: what if someone else already put in the value?
                # we do a check in vaex if it differs
                # but we could also store a Future
                self.storage[key] = new_value
                return new_value
            else:
                # although we don't use the return value directly, it's still used on the next time result_thread is
                # returned.
                return value

        result_thread: widget.Result[R] = widget.use_thread(do_work, dependencies=[key], intrusive_cancel=self.intrusive_cancel)
        if value is _DOES_NOT_EXIST:
            return result_thread
        else:
            self.hits += 1
            # what are the semantics of cancel and retry here?
            return widget.Result(value, state=widget.ResultState.FINISHED)


@overload
def memoize(
    function: None = None,
    key: None = None,
    storage: Optional[Storage] = None,
    allow_nonlocals=False,
) -> Callable[[Callable[P, R]], MemoizedFunction[P, R]]:
    ...


@overload
def memoize(
    function: None = None,
    key: Callable[P, R] = ...,
    storage: Optional[Storage] = None,
    allow_nonlocals=False,
) -> Callable[[Callable[P, R]], MemoizedFunction[P, R]]:
    ...


@overload
def memoize(
    function: Callable[P, R],
    key: None = None,
    storage: None = None,
    allow_nonlocals=False,
) -> MemoizedFunction[P, R]:
    ...


def memoize(
    function: Union[None, Callable[P, R]] = None,
    key: Union[None, Callable[P, R]] = None,
    storage: Optional[Storage] = None,
    allow_nonlocals: bool = False,
) -> Union[Callable[[Callable[P, R]], MemoizedFunction[P, R]], MemoizedFunction[P, R]]:
    """Will cache function return values based on the arguments.

    Example:

    ```python
    @widget.memoize
    def mean(values):
         return sum(values) / len(values)
    ```

    If a key function is provided, it will be used to generate the cache key based on the arguments instead.
    This is useful in situations where the arguments are not hashable, but a unique key can be generated
    based on the arguments.

    Also used in situations where the arguments are expensive to hash, but a cheaper key
    that is unique exists. For example using the filename instead of the file content.

    Example:

    ```python
    @widget.memoize(key=lambda df, column: (id(df), column))
    def mean(df, column):
        return df[column].mean()
    ```

    Without the key function, the above would fail because a DataFrame is not hashable.

    The function name and function code are added to the argument based key, together making up a unique cache key.
    Nonlocals variables are not included in the key, and are not allowed by default. Pass `allow_nonlocals=True`
    to allow nonlocals variables, or add them as arguments to the function.
    Globals are by default allowed, and also not included in the key. Solara will try to detect if globals are
    changed, and if so, will raise a ValueError.

    If a storage is provided, it will be used to store the cached values. If no storage is provided, the
    shared storage will be used. This is useful in situations where the cache should be shared between
    different functions to avoid excessive memory usage by limiting the number of cache entries or the
    memory content.

    The storage can be any object that implements the MutableMapping interface, for instance a dict or
    a cachetools.LRUCache. Or a new instance of `widget.cache.Memory`, see [caching](/docs/reference/caching)
    for cache storage options.

    The return value of the decorator behaves like the original function, but also has a few attributes:

     * `storage`: the storage used to cache the values
     * `key`: the key function used to generate the key
     * `function`: the original function
     * `use_thread`: a hook that will execute the function in a thread, and return a Result object
        If the value is already cached, the function will not be executed in a thread.


    See also the [reference on caching](/docs/reference/caching) for more caching details.

    """

    def wrapper(func: Callable[P, R]) -> MemoizedFunction[P, R]:
        return MemoizedFunction[P, R](
            func,
            cast(Callable[P, R], key or _default_key),
            storage,
            allow_nonlocals,
        )

    if function is None:
        return wrapper
    else:
        return wrapper(function)


cache_type_map = {
    "memory": "nextpy.interfaces.jupyter.cache.Memory",
    "memory-size": "solara_enterprise.cache.memory_size.MemorySize",
    "disk": "solara_enterprise.cache.disk.Disk",
    "redis": "solara_enterprise.cache.redis.Redis",
    "multi-level": "solara_enterprise.cache.multi_level.MultiLevel",
}


def create(name: str = "memory", *args, **kwargs) -> Storage:
    """Create a cache storage based on the name.

    ## Arguments

     - `name`: the name of the cache type, can be one of `memory`, `memory-size`, `disk`, `redis`, `multi-level`
     - `*args`: the arguments to pass to the cache constructor
     - `**kwargs`: the keyword arguments to pass to the cache constructor

    """
    if "," in name:
        names = name.split(",")
        logger.info("Set multilevel cache to %r", names)
        caches = []
        for name in names:
            caches.append(create(name, *args, **kwargs))
        cache = create("multi-level", *caches)
    elif name in cache_type_map:
        cls = widget.util.import_item(cache_type_map[name])
        cache = cls(*args, **kwargs)
    else:
        raise ValueError(f"Unknown type of cache {name}")
    return cache

storage: Storage = create(widget.settings.cache.type)


def configure(name="memory", *args, **kwargs):
    """Shorthand for widget.cache.storage = widget.cache.create(name, *args, **kwargs)"""
    global storage
    storage = create(name, *args, **kwargs)
