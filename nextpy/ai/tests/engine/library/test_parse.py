# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from nextpy.ai import engine


def test_parse():
    """Test the basic behavior of `parse`."""
    program = engine("""This is parsed: {{parse template}}""")
    assert (
        str(program(template="My name is {{name}}", name="Bob"))
        == "This is parsed: My name is Bob"
    )


def test_parse_with_name():
    program = engine("""This is parsed: {{parse template name="parsed"}}""")
    executed_program = program(template="My name is {{name}}", name="Bob")
    assert executed_program["parsed"] == "My name is Bob"
