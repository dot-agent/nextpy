from nextpy.ai import engine


def test_clear():
    """Makes sure we call clear."""
    engine.llms.OpenAI.cache.clear()
