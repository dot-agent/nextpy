from asyncio import AbstractEventLoop
from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openagent.gui.emitter import GuiEmitter


class GuiContextException(Exception):
    def __init__(self, msg="Gui context not found", *args, **kwargs):
        super().__init__(msg, *args, **kwargs)


emitter_var: ContextVar["GuiEmitter"] = ContextVar("emitter")
loop_var: ContextVar[AbstractEventLoop] = ContextVar("loop")


def get_emitter() -> "GuiEmitter":
    try:
        return emitter_var.get()
    except LookupError:
        raise GuiContextException()


def get_loop() -> AbstractEventLoop:
    try:
        return loop_var.get()
    except LookupError:
        raise GuiContextException()
