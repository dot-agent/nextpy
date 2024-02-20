# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from nextpy.ai import engine


def test_contains():
    """Test the behavior of `contains`."""
    program = engine(
        """{{#if (contains val "substr")}}are equal{{else}}not equal{{/if}}"""
    )
    assert str(program(val="no sub")) == "not equal"
    assert str(program(val="this is a substr")) == "are equal"
    assert str(program(val="this is a subsr")) == "not equal"
