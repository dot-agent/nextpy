from nextpy.ai import engine


def test_set():
    """Test the behavior of `set`."""
    program = engine("""{{set 'output' 234 hidden=False}}{{output}}""")
    assert str(program()) == "234234"

    program = engine("""{{set 'output' 234}}{{output}}""")
    assert str(program()) == "234"

    program = engine("""{{set 'output' 849203984939}}{{output}}""")
    assert str(program()["output"]) == "849203984939"


def test_set_dict():

    program = engine("""{{set {'output':234}}}{{output}}""")
    assert str(program()) == "234"


def test_set_array():

    program = engine("""{{set 'output' [3, 234]}}{{output}}""")
    assert str(program()) == "[3, 234]"
