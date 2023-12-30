# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import pytest

from nextpy.frontend.components.base.bare import Bare


@pytest.mark.parametrize(
    "contents,expected",
    [
        ("hello", "hello"),
        ("{}", "{}"),
        ("${default_state.name}", "${default_state.name}"),
        ("{state.name}", "{state.name}"),
    ],
)
def test_fstrings(contents, expected):
    """Test that fstrings are rendered correctly.

    Args:
        contents: The contents of the component.
        expected: The expected output.
    """
    comp = Bare.create(contents).render()
    assert comp["contents"] == expected
