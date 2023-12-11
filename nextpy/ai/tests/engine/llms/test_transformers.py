import pytest

from nextpy.ai import engine

from ..utils import get_llm


@pytest.mark.parametrize("llm", ["transformers:gpt2", "transformers:facebook/opt-350m"])
def test_basic(llm):
    llm = get_llm(llm)
    with llm.session() as s:
        out = s("this is a test", max_tokens=5)
        print(out)


def test_basic_object_init():
    llm = get_llm("transformers:gpt2")
    with llm.session() as s:
        out = s("this is a test", max_tokens=5)
        print(out)


@pytest.mark.parametrize("llm", ["transformers:gpt2", "transformers:facebook/opt-350m"])
def test_repeat(llm):
    llm = get_llm(llm)
    with llm.session() as s:
        s("this is a test", max_tokens=5)
        out2 = s("this is a test like another", max_tokens=5)
        print(out2)


@pytest.mark.parametrize("llm", ["transformers:gpt2", "transformers:facebook/opt-350m"])
def test_select(llm):
    llm = get_llm(llm)
    program = engine(
        '''Answer "yes" or "no": "{{#select 'answer'}}yes{{or}}no{{/select}}"''',
        llm=llm,
    )
    out = program()
    assert out["answer"] in ["yes", "no"]
