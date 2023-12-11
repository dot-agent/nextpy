import pytest

from nextpy.ai import engine

# Add this code to check if libraries are installed
try:
    import torch
    import transformers
except ImportError:
    torch = None
    transformers = None


def test_basic():
    """Test the basic behavior of the MPTChat model."""
    # skip if no GPU or torch/transformers not available
    if torch is None or not torch.cuda.is_available() or transformers is None:
        pytest.skip(
            "No GPU or transformers package not available, so skipping large model test."
        )

    # just make sure it runs
    llm = engine.llms.transformers.MPTChat("mosaicml/mpt-7b-chat", device=0)
    out = engine(
        """
{{#system~}}
You are an assistant.
{{~/system}}

{{#user~}}
How tall is the Eiffel Tower?
{{~/user}}

{{#assistant~}}
{{gen 'answer' max_tokens=10}}
{{~/assistant}}
""",
        llm=llm,
    )()

    assert len(out["answer"]) > 0
