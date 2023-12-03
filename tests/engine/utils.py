import pytest
from openams import engine
# import vertexai.language_models as palm

opanai_model_cache = {}
palm_model_cache = {}
transformers_model_cache = {}

def get_llm(model_name, caching=False, **kwargs):
    """Get an LLM by name."""
    if model_name.startswith("openai:"):
        return get_openai_llm(model_name[7:], caching, **kwargs)
    elif model_name.startswith("transformers:"):
        return get_transformers_llm(model_name[13:], caching, **kwargs)
    elif model_name.startswith("palm:"):
        return get_palm_llm(model_name[5:], caching, **kwargs)
    else:
        raise ValueError(f"Unsupported model type: {model_name}")

def get_palm_llm(model_name, caching=False, **kwargs):
    """Get a Palm LLM with model reuse."""
    key = f'{model_name}_{caching}'
    if key not in palm_model_cache:
        try:
            if not kwargs.get("rest_call", False):
                dummy_call = palm.ChatModel.from_pretrained("chat-bison")
            palm_model_cache[key] = engine.endpoints.PaLM(model_name, caching=caching, **kwargs)
        except Exception as e:
            pytest.skip(f"Failed to initialize PaLM model: {e}")

    llm = palm_model_cache[key]
    if llm.rest_call and (llm.api_key is None or llm.project_id is None):
        pytest.skip("PaLM token/project_id not found")

    return llm

def get_openai_llm(model_name, caching=False, **kwargs):
    """Get an OpenAI LLM with model reuse."""
    key = f'{model_name}_{caching}'
    if key not in opanai_model_cache:
        opanai_model_cache[key] = engine.endpoints.OpenAI(model_name, caching=caching, **kwargs)
        if opanai_model_cache[key].api_key is None:
            pytest.skip("OpenAI token not found")

    return opanai_model_cache[key]

def get_transformers_llm(model_name, caching=False):
    """Get a Transformers LLM with model reuse."""
    key = f'{model_name}_{caching}'
    if key not in transformers_model_cache:
        transformers_model_cache[key] = engine.endpoints.Transformers(model_name, caching=caching)

    return transformers_model_cache[key]
