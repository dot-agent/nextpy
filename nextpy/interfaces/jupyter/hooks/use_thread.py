import functools
import inspect
import logging
import os
import threading
from typing import Callable, Iterator, Optional, TypeVar, Union, cast

import nextpy.interfaces.jupyter as widget
from nextpy.interfaces.jupyter.datatypes import Result, ResultState
from nextpy.interfaces.jupyter.util import cancel_guard, nullcontext

SOLARA_ALLOW_OTHER_TRACER = os.environ.get("SOLARA_ALLOW_OTHER_TRACER", False) in (True, "True", "true", "1")
T = TypeVar("T")
logger = logging.getLogger("widget.hooks.use_thread")


def use_thread(
    callback=Union[
        Callable[[threading.Event], T],
        Iterator[Callable[[threading.Event], T]],
        Callable[[], T],
        Iterator[Callable[[], T]],
    ],
    dependencies=[],
    intrusive_cancel=True,
) -> Result[T]:
    from .misc import use_force_update, use_retry

    def make_event(*_ignore_dependencies):
        return threading.Event()

    def make_lock():
        return threading.Lock()

    lock: threading.Lock = widget.use_memo(make_lock, [])
    updater = use_force_update()
    result_state, set_result_state = widget.use_state(ResultState.INITIAL)
    error = widget.use_ref(cast(Optional[Exception], None))
    result = widget.use_ref(cast(Optional[T], None))
    running_thread = widget.use_ref(cast(Optional[threading.Thread], None))
    counter, retry = use_retry()
    cancel: threading.Event = widget.use_memo(make_event, [*dependencies, counter])

    def run():
        set_result_state(ResultState.STARTING)

        def runner():
            wait_for_thread = None
            with lock:
                # if there is a current thread already, we'll need
                # to wait for it. copy the ref, and set ourselves
                # as the current one
                if running_thread.current:
                    wait_for_thread = running_thread.current
                running_thread.current = threading.current_thread()
            if wait_for_thread is not None:
                set_result_state(ResultState.WAITING)
                # don't start before the previous is stopped
                try:
                    wait_for_thread.join()
                except:  # noqa
                    pass
                if threading.current_thread() != running_thread.current:
                    # in case a new thread was started that also was waiting for the previous
                    # thread to st stop, we can finish this
                    return
            # we previously set current to None, but if we do not do that, we can still render the old value
            # while we can still show a loading indicator using the .state
            # result.current = None
            set_result_state(ResultState.RUNNING)

            sig = inspect.signature(callback)
            if sig.parameters:
                f = functools.partial(callback, cancel)
            else:
                f = callback
            try:
                try:
                    # we only use the cancel_guard context manager around
                    # the function calls to f. We don't want to guard around
                    # a call to react, since that might slow down rendering
                    # during rendering
                    with cancel_guard(cancel) if intrusive_cancel else nullcontext():
                        value = f()
                    if inspect.isgenerator(value):
                        while True:
                            try:
                                with cancel_guard(cancel) if intrusive_cancel else nullcontext():
                                    result.current = next(value)
                                    error.current = None
                            except StopIteration:
                                break
                            # assigning to the ref doesn't trigger a rerender, so do it manually
                            updater()
                        if threading.current_thread() == running_thread.current:
                            set_result_state(ResultState.FINISHED)
                    else:
                        result.current = value
                        error.current = None
                        if threading.current_thread() == running_thread.current:
                            set_result_state(ResultState.FINISHED)
                except Exception as e:
                    error.current = e
                    if threading.current_thread() == running_thread.current:
                        logger.exception(e)
                        set_result_state(ResultState.ERROR)
                    return
                except widget.util.CancelledError:
                    pass
                    # this means this thread is cancelled not be request, but because
                    # a new thread is running, we can ignore this
            finally:
                if threading.current_thread() == running_thread.current:
                    running_thread.current = None
                    logger.info("thread done!")
                    if cancel.is_set():
                        set_result_state(ResultState.CANCELLED)

        logger.info("starting thread: %r", runner)
        thread = threading.Thread(target=runner, daemon=True)
        thread.start()

        def cleanup():
            cancel.set()  # cleanup for use effect

        return cleanup

    widget.use_effect(run, dependencies + [counter])
    return Result[T](value=result.current, error=error.current, state=result_state, cancel=cancel.set, _retry=retry)
