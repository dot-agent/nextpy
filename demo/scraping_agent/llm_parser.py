import os

from dotenv import load_dotenv
from langchain.chains import (create_extraction_chain,
                              create_extraction_chain_pydantic)
from langchain.chat_models import ChatOpenAI

load_dotenv()

openai_api_key = "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"

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613",
                 openai_api_key=openai_api_key)


def extract(content: str, **kwargs):
   

    if 'schema_pydantic' in kwargs:
        response = create_extraction_chain_pydantic(
            pydantic_schema=kwargs["schema_pydantic"], llm=llm).run(content)
        response_as_dict = [item.dict() for item in response]

        return response_as_dict
    else:
        return create_extraction_chain(schema=kwargs["schema"], llm=llm).run(content)