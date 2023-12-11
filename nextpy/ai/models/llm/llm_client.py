import os
from abc import ABC, abstractmethod

from litellm import completion


class LLMClient(ABC):
    def __init__(self, api_key):
        self.api_key = api_key
        self.chat = self.Chat(self)

    class Chat(ABC):
        def __init__(self, parent):
            self.api_key = parent.api_key
            self.completions = self.Completions(self)

        class Completions(ABC):
            def __init__(self, parent):
                self.api_key = parent.api_key

            @abstractmethod
            def create(self, model, messages):
                pass


class OpenAI(LLMClient):
    class Chat(LLMClient.Chat):
        class Completions(LLMClient.Chat.Completions):
            def create(self, model, messages):
                os.environ["OPENAI_API_KEY"] = self.api_key
                response = completion(model=model, messages=messages)
                return response


class Azure(LLMClient):
    class Chat(LLMClient.Chat):
        class Completions(LLMClient.Chat.Completions):
            def create(self, model, messages):
                os.environ["AZURE_API_KEY"] = self.api_key
                os.environ["AZURE_API_BASE"] = "your-azure-api-base"
                os.environ["AZURE_API_VERSION"] = "your-azure-api-version"
                response = completion(model=model, messages=messages)
                return response


# Usage for OpenAI
# openai_client = OpenAI(api_key="sk-") # Replace with your API key
# openai_response = openai_client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Hello!"}
#     ]
# )
# # Print the OpenAI response
# print(openai_response["choices"][0]["message"])
