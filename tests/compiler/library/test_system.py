from openagent import compiler

def test_system():
    """ Basic test of `system`.
    """

    llm = compiler.endpoints.Mock("the output")

    program = compiler("""
{{~#system}}You are fake.{{/system}}
{{#user}}You are real.{{/user}}
{{#assistant}}{{gen 'output' save_prompt='prompt'}}{{/assistant}}""", llm=llm)
    out = program()
    assert str(out).startswith('<|im_start|>system\nYou are fake.<|im_end|>')