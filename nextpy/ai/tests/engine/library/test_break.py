# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from nextpy.ai import engine


def test_break_each():
    """Test the behavior of `break` in an `each` loop."""
    llm = engine.llms.Mock()
    program = engine(
        """Loop to ten:
{{~#each list}}
{{this}}
{{~#if (equal this 5)}}{{break}}{{/if~}}
{{/each}}""",
        llm=llm,
    )
    out = program(list=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    assert out.text == "Loop to ten:\n1\n2\n3\n4\n5"
