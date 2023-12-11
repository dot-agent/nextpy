from nextpy.ai import engine


def test_greater():
    """Test the behavior of `greater`."""
    program = engine("""{{#if (greater val 5)}}greater{{else}}not greater{{/if}}""")
    assert str(program(val=4)) == "not greater"
    assert str(program(val=6)) == "greater"
    assert str(program(val=5.3)) == "greater"


def test_greater_infix():
    program = engine("""{{#if val > 5}}greater{{else}}not greater{{/if}}""")
    assert str(program(val=4)) == "not greater"
    assert str(program(val=6)) == "greater"
    assert str(program(val=5.3)) == "greater"
