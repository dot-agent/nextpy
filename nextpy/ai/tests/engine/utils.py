# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import pytest

from nextpy.ai import engine

try:
    import torch
    import transformers
except ImportError:
    transformers = None
    torch = None

opanai_model_cache = {}


def get_llm(model_name, caching=False, **kwargs):
    """Get an LLM by name."""
    if model_name.startswith("openai:"):
        return get_openai_llm(model_name[7:], caching, **kwargs)
    elif model_name.startswith("transformers:"):
        return get_transformers_llm(model_name[13:], caching, **kwargs)
    else:
        raise ValueError(f"Unknown llm: {model_name}")


def get_openai_llm(model_name, caching=False, **kwargs):
    """Get an OpenAI LLM with model reuse and smart test skipping."""
    # we cache the models so lots of tests using the same model don't have to
    # load it over and over again
    key = model_name + "_" + str(caching)
    if key not in opanai_model_cache:
        opanai_model_cache[key] = engine.llms.OpenAI(
            model_name, caching=caching, **kwargs
        )
    llm = opanai_model_cache[key]

    if llm.api_key is None:
        pytest.skip("OpenAI token not found")

    return llm


transformers_model_cache = {}


def get_transformers_llm(model_name, caching=False):
    """Get an OpenAI LLM with model reuse."""
    if transformers is None:
        pytest.skip("transformers package required")

    key = model_name + "_" + str(caching)
    if key not in transformers_model_cache:
        transformers_model_cache[key] = engine.llms.Transformers(
            model_name, caching=caching
        )

    return transformers_model_cache[key]
