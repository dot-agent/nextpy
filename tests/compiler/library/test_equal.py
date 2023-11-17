from openagent import compiler

def test_equal():
    """ Test the behavior of `equal`.
    """

    program = compiler("""{{#if (equal val 5)}}are equal{{else}}not equal{{/if}}""")
    assert str(program(val=4)) == "not equal"
    assert str(program(val=5)) == "are equal"
    assert str(program(val="5")) == "not equal"

def test_equal_infix():
    program = compiler("""{{#if val == 5}}are equal{{else}}not equal{{/if}}""")
    assert str(program(val=4)) == "not equal"
    assert str(program(val=5)) == "are equal"
    assert str(program(val="5")) == "not equal"