# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.


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