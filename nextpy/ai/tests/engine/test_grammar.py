from nextpy.ai import engine


def test_variable_interpolation():
    """Test variable interpolation in prompt."""
    prompt = engine("Hello, {{name}}!")
    assert str(prompt(name="Compiler")) == "Hello, Compiler!"


def test_command_call():
    prompt = engine("Hello, {{add 1 2}}!")
    assert str(prompt(name="Compiler")) == "Hello, 3!"


def test_paren_command_call():
    prompt = engine("Hello, {{add(1, 2)}}!")
    assert str(prompt(name="Compiler")) == "Hello, 3!"


def test_nested_command_call():
    prompt = engine("Hello, {{add (add 1 2) 3}}!")
    assert str(prompt(name="Compiler")) == "Hello, 6!"


def test_nested_paren_command_call():
    prompt = engine("Hello, {{add add(1, 2) 3}}!")
    assert str(prompt(name="Compiler")) == "Hello, 6!"


def test_infix_plus():
    prompt = engine("Hello, {{1 + 2}}!")
    assert str(prompt()) == "Hello, 3!"


def test_infix_plus_nested():
    prompt = engine("Hello, {{set 'variable' 1 + 2}}!")
    assert prompt()["variable"] == 3


def test_comment():
    prompt = engine("Hello, {{! this is a comment}}Bob!")
    assert str(prompt()) == "Hello, Bob!"


def test_comment2():
    prompt = engine("Hello, {{! this is a comment}}Bob!{{@prefix}}")
    assert str(prompt()) == "Hello, Bob!Hello, Bob!"


def test_long_comment():
    prompt = engine("Hello, {{!-- this is a comment --}}Bob!{{@prefix}}")
    assert str(prompt()) == "Hello, Bob!Hello, Bob!"


def test_long_comment_ws_strip():
    prompt = engine("Hello, {{~!-- this is a comment --~}} Bob!{{@prefix}}")
    assert str(prompt()) == "Hello,Bob!Hello,Bob!"


def test_comment_ws_strip():
    prompt = engine("Hello, {{~! this is a comment ~}} Bob!{{@prefix}}")
    assert str(prompt()) == "Hello,Bob!Hello,Bob!"


def test_escape_command():
    prompt = engine("Hello, \\{{command}} Bob!")
    assert str(prompt()) == "Hello, {{command}} Bob!"


def test_indexing():
    prompt = engine("Hello, {{arr[0]}} Bob!")
    assert str(prompt(arr=["there"])) == "Hello, there Bob!"


def test_special_var():
    prompt = engine("{{#each arr}}Hello, {{@index}}-{{this}}!{{/each}}")
    assert str(prompt(arr=["there"])) == "Hello, 0-there!"

    prompt = engine("{{#geneach 'arr' num_iterations=1}}Hello, {{@index}}!{{/each}}")
    assert str(prompt(arr=["there"])) == "Hello, 0!"


def test_special_var_index():
    prompt = engine("{{#each arr}}{{arr[@index]}}{{/each}}!")
    assert str(prompt(arr=["there"])) == "there!"
    prompt = engine("{{#geneach 'out' num_iterations=1}}{{arr[@index]}}{{/each}}!")
    assert str(prompt(arr=["there"])) == "there!"
