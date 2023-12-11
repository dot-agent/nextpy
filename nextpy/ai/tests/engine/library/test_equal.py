from nextpy.ai import engine


def test_equal():
    """Test the behavior of `equal`."""
    program = engine("""{{#if (equal val 5)}}are equal{{else}}not equal{{/if}}""")
    assert str(program(val=4)) == "not equal"
    assert str(program(val=5)) == "are equal"
    assert str(program(val="5")) == "not equal"


def test_equal_infix():
    program = engine("""{{#if val == 5}}are equal{{else}}not equal{{/if}}""")
    assert str(program(val=4)) == "not equal"
    assert str(program(val=5)) == "are equal"
    assert str(program(val="5")) == "not equal"
