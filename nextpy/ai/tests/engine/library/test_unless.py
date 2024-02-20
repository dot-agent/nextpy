# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import pytest

from nextpy.ai import engine


@pytest.mark.parametrize(
    "flag, expected_output",
    [
        (True, "Answer: "),
        (1, "Answer: "),
        ("random text", "Answer: "),
        (False, "Answer: Yes"),
        (0, "Answer: Yes"),
        ("", "Answer: Yes"),
    ],
)
def test_unless(flag, expected_output):
    """Test the behavior of `unless`."""
    program = engine("""Answer: {{#unless flag}}Yes{{/unless}}""")
    out = program(flag=flag)
    assert str(out) == expected_output
