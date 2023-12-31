# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from nextpy.ai import engine


def test_if():
    """Test the behavior of `if`."""
    prompt = engine("""Answer: {{#if flag}}Yes{{/if}}""")

    for flag in [True, 1, "random text"]:
        out = prompt(flag=flag)
        assert str(out) == "Answer: Yes"

    for flag in [False, 0, ""]:
        out = prompt(flag=flag)
        assert str(out) == "Answer: "


def test_if_complex_block():
    prompt = engine("""Answer: {{#if True}}Yes {{my_var}} we{{/if}}""")

    out = prompt(my_var="then")

    assert str(out) == "Answer: Yes then we"


def test_if_else():
    """Test the behavior of `if` with an `else` clause."""
    prompt = engine("""Answer 'Yes' or 'No': '{{#if flag}}Yes{{else}}No{{/if}}'""")

    for flag in [True, 1, "random text"]:
        out = prompt(flag=flag)
        assert str(out) == "Answer 'Yes' or 'No': 'Yes'"

    for flag in [False, 0, ""]:
        out = prompt(flag=flag)
        assert str(out) == "Answer 'Yes' or 'No': 'No'"


def test_if_complex_blockwith_else():
    prompt = engine(
        """Answer: {{#if flag}}Yes {{my_var}} we{{else}}No {{my_var}}{{/if}}"""
    )

    out = prompt(my_var="then", flag=True)
    assert str(out) == "Answer: Yes then we"

    out = prompt(my_var="then", flag=False)
    assert str(out) == "Answer: No then"


def test_elif_else():
    """Test the behavior of `if` with an `else` clause."""
    prompt = engine(
        """Answer 'Yes' or 'No': '{{#if flag}}Yes{{elif flag2}}maybe{{else}}No{{/if}}'"""
    )

    out = prompt(flag=False, flag2=True)
    assert str(out) == "Answer 'Yes' or 'No': 'maybe'"
