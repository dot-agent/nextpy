from dotagent import compiler
import pytest

def test_basic():
    """ Test the basic behavior of the LLaMA model.
    """

    # skip if no GPU
    import torch
    if torch.cuda.device_count() == 0:
        pytest.skip("No GPU, so skipping large model test.")

    # just make sure it runs
    llm = compiler.llms.transformers.LLaMA('../../models/llama/7B', device=1)
    out = compiler("""The height of the Sears tower is {{gen 'answer' max_tokens=10}}""", llm=llm)()
    assert len(out["answer"]) > 0