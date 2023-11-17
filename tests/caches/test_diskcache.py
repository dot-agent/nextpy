from openagent import compiler

def test_clear():
    """Makes sure we call clear"""
    compiler.llms.OpenAI.cache.clear()