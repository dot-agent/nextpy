from dotagent import compiler

def test_variable_interpolation():
    """ Test variable interpolation in prompt
    """

    prompt = compiler("Hello, {{name}}!")
    assert str(prompt(name="Compiler")) == "Hello, Compiler!"

def test_command_call():
    prompt = compiler("Hello, {{add 1 2}}!")
    assert str(prompt(name="Compiler")) == "Hello, 3!"

def test_paren_command_call():
    prompt = compiler("Hello, {{add(1, 2)}}!")
    assert str(prompt(name="Compiler")) == "Hello, 3!"

def test_nested_command_call():
    prompt = compiler("Hello, {{add (add 1 2) 3}}!")
    assert str(prompt(name="Compiler")) == "Hello, 6!"

def test_nested_paren_command_call():
    prompt = compiler("Hello, {{add add(1, 2) 3}}!")
    assert str(prompt(name="Compiler")) == "Hello, 6!"

def test_infix_plus():
    prompt = compiler("Hello, {{1 + 2}}!")
    assert str(prompt()) == "Hello, 3!"

def test_infix_plus_nested():
    prompt = compiler("Hello, {{set 'variable' 1 + 2}}!")
    assert prompt()["variable"] == 3

def test_comment():
    prompt = compiler("Hello, {{! this is a comment}}Bob!")
    assert str(prompt()) == "Hello, Bob!"

def test_comment2():
    prompt = compiler("Hello, {{! this is a comment}}Bob!{{@prefix}}")
    assert str(prompt()) == "Hello, Bob!Hello, Bob!"

def test_long_comment():
    prompt = compiler("Hello, {{!-- this is a comment --}}Bob!{{@prefix}}")
    assert str(prompt()) == "Hello, Bob!Hello, Bob!"

def test_long_comment_ws_strip():
    prompt = compiler("Hello, {{~!-- this is a comment --~}} Bob!{{@prefix}}")
    assert str(prompt()) == "Hello,Bob!Hello,Bob!"

def test_comment_ws_strip():
    prompt = compiler("Hello, {{~! this is a comment ~}} Bob!{{@prefix}}")
    assert str(prompt()) == "Hello,Bob!Hello,Bob!"

def test_escape_command():
    prompt = compiler("Hello, \{{command}} Bob!")
    assert str(prompt()) == "Hello, {{command}} Bob!"

def test_indexing():
    prompt = compiler("Hello, {{arr[0]}} Bob!")
    assert str(prompt(arr=["there"])) == "Hello, there Bob!"

def test_special_var():
    prompt = compiler("{{#each arr}}Hello, {{@index}}-{{this}}!{{/each}}")
    assert str(prompt(arr=["there"])) == "Hello, 0-there!"

    prompt = compiler("{{#geneach 'arr' num_iterations=1}}Hello, {{@index}}!{{/each}}")
    assert str(prompt(arr=["there"])) == "Hello, 0!"

def test_special_var_index():
    prompt = compiler("{{#each arr}}{{arr[@index]}}{{/each}}!")
    assert str(prompt(arr=["there"])) == "there!"
    prompt = compiler("{{#geneach 'out' num_iterations=1}}{{arr[@index]}}{{/each}}!")
    assert str(prompt(arr=["there"])) == "there!"