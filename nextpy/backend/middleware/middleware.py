"""Base Nextpy middleware."""
from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Optional

from nextpy.backend.event import Event
from nextpy.backend.state import BaseState, StateUpdate
from nextpy.base import Base

if TYPE_CHECKING:
    from nextpy.app import App


class Middleware(Base, ABC):
    """Middleware to preprocess and postprocess requests."""

    async def preprocess(
        self, app: App, state: BaseState, event: Event
    ) -> Optional[StateUpdate]:
        """Preprocess the event.

        Args:
            app: The app.
            state: The client state.
            event: The event to preprocess.

        Returns:
            An optional state update to return.
        """
        return None

    async def postprocess(
        self, app: App, state: BaseState, event: Event, update: StateUpdate
    ) -> StateUpdate:
        """Postprocess the event.

        Args:
            app: The app.
            state: The client state.
            event: The event to postprocess.
            update: The current state update.

        Returns:
            An optional state to return.
        """
        return update
