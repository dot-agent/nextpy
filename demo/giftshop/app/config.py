import openai
from .env import OPENAI_API_KEY, SERPAPI_KEY

class Config:
    openai_key = OPENAI_API_KEY
    serpapi_key = SERPAPI_KEY
    
    @staticmethod
    def get_openai_key():
        return Config.openai_key
    
    @staticmethod
    def get_serpapi_key():
        return Config.serpapi_key


