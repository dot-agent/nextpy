# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from nextpy.ai import engine


def test_assistant():
    """Basic test of `assistant`."""
    llm = engine.llms.Mock("the output")

    program = engine(
        """
{{#system}}You are fake.{{/system}}
{{#user}}You are real.{{/user}}
{{#assistant}}{{gen 'output' save_prompt='prompt'}}{{/assistant}}""",
        llm=llm,
    )
    out = program()
    assert out["output"] == "the output"
    # assert str(out) == '\n<|im_start|>system\nYou are fake.<|im_end|>\n<|im_start|>user\nYou are real.<|im_end|>\n<|im_start|>assistant\nthe output<|im_end|>'
