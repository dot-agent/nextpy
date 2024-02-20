# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from nextpy.ai import engine


def test_role():
    """Test the behavior of `role`."""
    llm = engine.llms.Mock()
    prompt = engine(
        """
{{#role 'system'~}}
You are an assistant.
{{~/role}}

{{#role 'user'~}}
What is the weather?
{{~/role}}

{{#role 'assistant'~}}
{{gen(max_tokens=23)}}
{{~/role}}
""",
        llm=llm,
    )

    out = prompt()
    assert (
        str(out)
        == "\n<|im_start|>system\nYou are an assistant.<|im_end|>\n\n<|im_start|>user\nWhat is the weather?<|im_end|>\n\n<|im_start|>assistant\nmock output 0<|im_end|>\n"
    )


def test_short_roles():
    """Test the behavior of the shorthand versions of `role`."""
    llm = engine.llms.Mock()
    prompt = engine(
        """
{{#system~}}
You are an assistant.
{{~/system}}

{{#user~}}
What is the weather?
{{~/user}}

{{#assistant~}}
{{gen()}}
{{~/assistant}}
""",
        llm=llm,
    )

    out = prompt(test="asdfa")
    assert (
        str(out)
        == "\n<|im_start|>system\nYou are an assistant.<|im_end|>\n\n<|im_start|>user\nWhat is the weather?<|im_end|>\n\n<|im_start|>assistant\nmock output 0<|im_end|>\n"
    )
