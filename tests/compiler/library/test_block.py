from dotagent import compiler
from ...utils import get_llm

def test_hidden_block():
    """ Test the behavior of generic `block`.
    """

    prompt = compiler("""This is a test {{#block hidden=True}}example{{/block}}""")
    out = prompt()
    assert out.text == "This is a test "

def test_empty_block():
    """ Test the behavior of a completely empty `block`.
    """

    prompt = compiler(
        "{{#block}}{{#if nonempty}}{{nonempty}}{{/if}}{{/block}}",
    )
    out = prompt(nonempty=False)
    assert out.text == ''

def test_name_capture():
    prompt = compiler(
        "This is a block: {{#block 'my_block'}}text inside block{{/block}}",
    )
    out = prompt()
    assert out["my_block"] == 'text inside block'

def test_name_capture_whitespace():
    prompt = compiler(
        "This is a block: {{#block 'my_block'}} text inside block {{/block}}",
    )
    out = prompt()
    assert out["my_block"] == ' text inside block '