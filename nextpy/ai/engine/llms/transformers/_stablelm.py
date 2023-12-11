
from .._transformers import Transformers

class StableLMChat(Transformers):
    """ A HuggingFace transformers version of the StableLM language model with Compiler support.
    """

    llm_name: str = "stablelm"

    @staticmethod
    def role_start(role):
        return "<|"+role.upper()+"|>"
    
    @staticmethod
    def role_end(role):
        return '' 