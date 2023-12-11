"""Utility functions for API requests."""

import json
from io import BytesIO
from typing import Optional

import requests
from aiohttp import ClientResponse, ClientSession, FormData
from aiohttp.payload import BytesIOPayload

from nextpy.ai.config import settings


class AgentBoxError(Exception):
    """Represents an api error returned from the AgentBox API."""

    def __init__(
        self,
        http_status: int = 0,
        json_body: dict = {},
        headers: dict = {},
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers

    def __str__(self):
        return f"{self.http_status}: {self.json_body}"

    def __repr__(self):
        return f"<AgentBoxError {self.http_status}: {self.json_body}>"


def build_agentbox_request_data(
    method: str,
    endpoint: str,
    body: Optional[dict] = None,
    files: Optional[dict] = None,
) -> dict:
    """Builds a request data dictionary for the requests library."""
    return {
        "method": method,
        "url": settings.AGENTBOX_BASE_URL + endpoint,
        "headers": {
            "Authorization": f"Bearer {settings.AGENTBOX_API_KEY}",
        },
        "json": body,
        "files": files,
    }


def handle_agentbox_response(response: requests.Response):
    """Handles a response from the requests library."""
    handlers = {
        "application/json": lambda r: json.loads(r.content.decode()),
        "application/octet-stream": lambda r: {
            "content": BytesIO(r.content).read(),
            "name": r.headers["Content-Disposition"].split("=")[1],
        }
        # Add other content type handlers here
    }
    handler = handlers.get(
        response.headers["Content-Type"].split(";")[0], lambda r: r.content.decode()
    )
    if response.status_code != 200:
        raise AgentBoxError(
            http_status=response.status_code,
            json_body=response.json(),
            headers=response.headers.__dict__,
        )
    return handler(response)


async def handle_response_async(response: ClientResponse) -> dict:
    """Handles a response from the aiohttp library."""

    async def json_handler(r: ClientResponse) -> dict:
        return json.loads(await r.text())

    async def file_handler(r: ClientResponse) -> dict:
        return {
            "content": await r.read(),
            "name": r.headers["Content-Disposition"].split("=")[1],
        }

    async def default_handler(r: ClientResponse) -> dict:
        return {"content": await r.text()}

    handlers = {
        "application/json": json_handler,
        "application/octet-stream": file_handler,
        # Add other content type handlers here
    }
    handler = handlers.get(
        response.headers["Content-Type"].split(";")[0], default_handler
    )
    if response.status != 200:
        raise AgentBoxError(
            http_status=response.status,
            json_body=await response.json(),
            headers=response.headers.__dict__,
        )
    return await handler(response)


def base_request(
    method: str,
    endpoint: str,
    body: Optional[dict] = None,
    files: Optional[dict] = None,
) -> dict:
    """Makes a request to the AgentBox API."""
    request_data = build_request_data(method, endpoint, body, files)
    response = requests.request(**request_data, timeout=90)
    return handle_response(response)


async def abase_request(
    session: ClientSession,
    method: str,
    endpoint: str,
    body: Optional[dict] = None,
    files: Optional[dict] = None,
) -> dict:
    """Makes an asynchronous request to the AgentBox API."""
    request_data = build_request_data(method, endpoint, body, files)
    if files is not None:
        data = FormData()
        for key, file_tuple in files.items():
            filename, fileobject = file_tuple[
                :2
            ]  # Get the filename and fileobject from the tuple
            payload = BytesIOPayload(BytesIO(fileobject))
            data.add_field(
                key, payload, filename=filename
            )  # Use the filename from the tuple
        request_data.pop("files")
        request_data.pop("json")
        request_data["data"] = data
        response = await session.request(**request_data)
    else:
        request_data.pop("files")
        response = await session.request(**request_data)
    return await handle_response_async(response)


def set_agentbox_api_key(api_key: str) -> None:
    """Manually set the AGENTBOX_API_KEY."""
    settings.AGENTBOX_API_KEY = api_key
