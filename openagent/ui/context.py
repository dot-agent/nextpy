from asyncio import AbstractEventLoop
from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openagent.ui.emitter import OpenagentUIEmitter


class OpenagentUIContextException(Exception):
    def __init__(self, msg="openagent.ui context not found", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


emitter_var: ContextVar["OpenagentUIEmitter"] = ContextVar("emitter")
loop_var: ContextVar[AbstractEventLoop] = ContextVar("loop")


def get_emitter() -> "OpenagentUIEmitter":
    try:
        return emitter_var.get()
    except LookupError:
        raise OpenagentUIContextException()


def get_loop() -> AbstractEventLoop:
    try:
        return loop_var.get()
    except LookupError:
        raise OpenagentUIContextException()
