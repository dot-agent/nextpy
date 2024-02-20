# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from nextpy.ai import engine


def test_strip():
    """Test the behavior of `strip`."""
    program = engine("""{{strip ' this is '}}""")
    assert str(program()) == "this is"
