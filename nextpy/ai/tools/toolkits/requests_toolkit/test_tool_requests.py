from typing import Any, Dict

import pytest

from nextpy.ai.tools.toolkits.requests_toolkit.requests.base import (
    RequestsDeleteTool,
    RequestsGetTool,
    RequestsPatchTool,
    RequestsPostTool,
    RequestsPutTool,
    _parse_input,
)
from nextpy.ai.tools.toolkits.requests_toolkit.requests.utils import TextRequestsWrapper


class _MockTextRequestsWrapper(TextRequestsWrapper):
    @staticmethod
    def get(url: str, **kwargs: Any) -> str:
        return "get_response"

    @staticmethod
    def post(url: str, data: Dict[str, Any], **kwargs: Any) -> str:
        return f"post {str(data)}"

    @staticmethod
    def patch(url: str, data: Dict[str, Any], **kwargs: Any) -> str:
        return f"patch {str(data)}"

    @staticmethod
    def put(url: str, data: Dict[str, Any], **kwargs: Any) -> str:
        return f"put {str(data)}"

    @staticmethod
    def delete(url: str, **kwargs: Any) -> str:
        return "delete_response"


@pytest.fixture
def mock_requests_wrapper() -> TextRequestsWrapper:
    return _MockTextRequestsWrapper()


def test_parse_input() -> None:
    input_text = '{"url": "https://example.com", "data": {"key": "value"}}'
    expected_output = {"url": "https://example.com", "data": {"key": "value"}}
    assert _parse_input(input_text) == expected_output


def test_requests_get_tool(mock_requests_wrapper: TextRequestsWrapper) -> None:
    tool = RequestsGetTool(requests_wrapper=mock_requests_wrapper)
    assert tool.run("https://example.com") == "get_response"


def test_requests_post_tool(mock_requests_wrapper: TextRequestsWrapper) -> None:
    tool = RequestsPostTool(requests_wrapper=mock_requests_wrapper)
    input_text = '{"url": "https://example.com", "data": {"key": "value"}}'
    assert tool.run(input_text) == "post {'key': 'value'}"


def test_requests_patch_tool(mock_requests_wrapper: TextRequestsWrapper) -> None:
    tool = RequestsPatchTool(requests_wrapper=mock_requests_wrapper)
    input_text = '{"url": "https://example.com", "data": {"key": "value"}}'
    assert tool.run(input_text) == "patch {'key': 'value'}"


def test_requests_put_tool(mock_requests_wrapper: TextRequestsWrapper) -> None:
    tool = RequestsPutTool(requests_wrapper=mock_requests_wrapper)
    input_text = '{"url": "https://example.com", "data": {"key": "value"}}'
    assert tool.run(input_text) == "put {'key': 'value'}"


def test_requests_delete_tool(mock_requests_wrapper: TextRequestsWrapper) -> None:
    tool = RequestsDeleteTool(requests_wrapper=mock_requests_wrapper)
    assert tool.run("https://example.com") == "delete_response"
