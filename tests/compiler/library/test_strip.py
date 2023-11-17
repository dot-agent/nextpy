from openagent import compiler

def test_strip():
    """ Test the behavior of `strip`.
    """

    program = compiler("""{{strip ' this is '}}""")
    assert str(program()) == "this is"