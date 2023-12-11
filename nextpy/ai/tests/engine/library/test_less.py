from nextpy.ai import engine


def test_less():
    """Test the behavior of `less`."""
    program = engine("""{{#if (less val 5)}}less{{else}}not less{{/if}}""")
    assert str(program(val=6)) == "not less"
    assert str(program(val=4)) == "less"
    assert str(program(val=4.3)) == "less"


def test_less_infix():
    """Test the behavior of `less` used as `<`."""
    program = engine("""{{#if val < 5}}less{{else}}not less{{/if}}""")
    assert str(program(val=6)) == "not less"
    assert str(program(val=4)) == "less"
    assert str(program(val=4.3)) == "less"
