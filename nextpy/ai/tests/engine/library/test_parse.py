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
