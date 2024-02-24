# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""The page decorator and associated variables and functions."""

from nextpy.frontend.components.component import Component
from nextpy.backend.event import EventHandler

DECORATED_PAGES: list

def page(
    route: str | None = None,
    title: str | None = None,
    image: str | None = None,
    description: str | None = None,
    meta: str | None = None,
    script_tags: list[Component] | None = None,
    on_load: EventHandler | list[EventHandler] | None = None,
): ...
def get_decorated_pages() -> list[dict]: ...
