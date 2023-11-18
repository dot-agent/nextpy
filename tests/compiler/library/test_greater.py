from openams import compiler

def test_greater():
    """ Test the behavior of `greater`.
    """

    program = compiler("""{{#if (greater val 5)}}greater{{else}}not greater{{/if}}""")
    assert str(program(val=4)) == "not greater"
    assert str(program(val=6)) == "greater"
    assert str(program(val=5.3)) == "greater"

def test_greater_infix():
    program = compiler("""{{#if val > 5}}greater{{else}}not greater{{/if}}""")
    assert str(program(val=4)) == "not greater"
    assert str(program(val=6)) == "greater"
    assert str(program(val=5.3)) == "greater"