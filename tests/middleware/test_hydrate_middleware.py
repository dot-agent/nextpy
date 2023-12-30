# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from __future__ import annotations

import pytest

from nextpy.app import App
from nextpy.backend.middleware.hydrate_middleware import HydrateMiddleware
from nextpy.backend.state import State, StateUpdate


class TestState(State):
    """A test state with no return in handler."""

    __test__ = False

    num: int = 0

    def test_handler(self):
        """Test handler."""
        self.num += 1


@pytest.fixture
def hydrate_middleware() -> HydrateMiddleware:
    """Fixture creates an instance of HydrateMiddleware per test case.

    Returns:
        instance of HydrateMiddleware
    """
    return HydrateMiddleware()


@pytest.mark.asyncio
async def test_preprocess_no_events(hydrate_middleware, event1, mocker):
    """Test that app without on_load is processed correctly.

    Args:
        hydrate_middleware: Instance of HydrateMiddleware
        event1: An Event.
        mocker: pytest mock object.
    """
    mocker.patch("nextpy.state.State.class_subclasses", {TestState})
    state = State()
    update = await hydrate_middleware.preprocess(
        app=App(state=State),
        event=event1,
        state=state,
    )
    assert isinstance(update, StateUpdate)
    assert update.delta == state.dict()
    assert not update.events
