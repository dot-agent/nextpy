from nextpy.ai import engine
from nextpy.ai.endpoints._openai import OpenAI

llm = OpenAI(model="gpt-4")

prompt = """
{{#system~}}
You are a helpful and terse assistant. 
{{~/system}}

{{#user~}}
Given a chunk of text, provide an informative summary in not more than {{max_words}} words.

{{input_text}}
{{~/user}}

{{#assistant~}}
{{gen 'response'}}
{{~/assistant}}

"""

engine = engine(prompt, llm=llm, silent=True)


class Summarizer:
    def __init__(self, engine=engine) -> None:

        self.engine = engine

    def summarize(self, input_text, max_words):

        result = self.engine(input_text=input_text, max_words=max_words)

        response = result["response"]

        return response
