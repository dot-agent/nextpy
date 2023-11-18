from openagent import compiler

def test_user():
    """ Basic test of `user`.
    """

    llm = compiler.endpoints.Mock("the output")

    program = compiler("""
{{~#system}}You are fake.{{/system}}
{{#user}}You are real.{{/user}}
{{#assistant}}{{gen 'output' save_prompt='prompt'}}{{/assistant}}""", llm=llm)
    out = program()
    assert '<|im_start|>user\nYou are real.<|im_end|>' in str(out)