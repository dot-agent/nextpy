from openams import compiler

def test_clear():
    """Makes sure we call clear"""
    compiler.endpoints.OpenAI.cache.clear()