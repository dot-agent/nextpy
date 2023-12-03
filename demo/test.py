# # Guaranteeing valid output syntax
#
# Large language models are great at generating useful outputs, but they are not great at guaranteeing that those outputs follow a specific format. This can cause problems when we want to use the outputs of a language model as input to another system. For example, if we want to use a language model to generate a JSON object, we need to make sure that the output is valid JSON. This can be a real pain with standard APIs, but with `engine` we can both accelerate inference speed and ensure that generated JSON is always valid.

from openams import engine

# we use LLaMA here, but any GPT-style model will do
engine.llm = engine.llms.Transformers(
    "PY007/TinyLlama-1.1B-Chat-v0.2", device=0, caching=False
)

program = engine(
    "1, 2, 3, 4, 5, {{#select 'num2'}}6{{or}}7{{or}}8{{or}}9{{/select}}. That's all."
)
out = program()
print(out)

program = engine(
    "1, 2, 3, 4, 5, {{#selectm 'num2' sep=', '}}6{{or}}7{{or}}8{{or}}9{{/selectm}}. That's all."
)
out = program()
print(out)