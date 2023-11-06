from dotagent import compiler

def test_set():
    """ Test the behavior of `set`.
    """

    program = compiler("""{{set 'output' 234 hidden=False}}{{output}}""")
    assert str(program()) == "234234"
    
    program = compiler("""{{set 'output' 234}}{{output}}""")
    assert str(program()) == "234"

    program = compiler("""{{set 'output' 849203984939}}{{output}}""")
    assert str(program()['output']) == "849203984939"

def test_set_dict():
    
    program = compiler("""{{set {'output':234}}}{{output}}""")
    assert str(program()) == "234"

def test_set_array():
    
    program = compiler("""{{set 'output' [3, 234]}}{{output}}""")
    assert str(program()) == "[3, 234]"