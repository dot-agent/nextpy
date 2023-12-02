from openams import engine

def test_clear():
    """Makes sure we call clear"""
    engine.endpoints.OpenAI.cache.clear()