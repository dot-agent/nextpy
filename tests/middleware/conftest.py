# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import pytest

from nextpy.backend.event import Event


def create_event(name):
    return Event(
        token="<token>",
        name=name,
        router_data={
            "pathname": "/",
            "query": {},
            "token": "<token>",
            "sid": "<sid>",
            "headers": {},
            "ip": "127.0.0.1",
        },
        payload={},
    )


@pytest.fixture
def event1():
    return create_event("state.hydrate")
