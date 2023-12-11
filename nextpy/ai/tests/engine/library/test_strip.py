from nextpy.ai import engine


def test_strip():
    """Test the behavior of `strip`."""
    program = engine("""{{strip ' this is '}}""")
    assert str(program()) == "this is"
