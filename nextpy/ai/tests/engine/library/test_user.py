# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from nextpy.ai import engine


def test_user():
    """Basic test of `user`."""
    llm = engine.llms.Mock("the output")

    program = engine(
        """
{{~#system}}You are fake.{{/system}}
{{#user}}You are real.{{/user}}
{{#assistant}}{{gen 'output' save_prompt='prompt'}}{{/assistant}}""",
        llm=llm,
    )
    out = program()
    assert "<|im_start|>user\nYou are real.<|im_end|>" in str(out)
