import math
import openai
from nextpy.utils.data_ops import get_from_dict_or_env

def gen_openai_completion(prompt: str):
    """
    Generates a completion using the OpenAI API.

    Args:
        prompt (str): The text prompt for the API.

    Returns:
        dict: The response from the OpenAI API.
    """
    try:
        openai_api_key = get_from_dict_or_env("OPENAI_API_KEY")
        openai.api_key = openai_api_key
        response = openai.Completion.create(
            model="text-davinci-003", prompt=prompt, max_tokens=0, echo=True, logprobs=0
        )
        return response
    except Exception as e:
        # Handle exceptions (e.g., API errors, network issues)
        print(f"Error in generating OpenAI completion: {e}")
        return None

def calculate_perplexity(prompt: str):
    """
    Calculates the perplexity of a given prompt.

    Args:
        prompt (str): The text prompt to calculate perplexity for.

    Returns:
        float: The perplexity of the prompt.
    """
    response = gen_openai_completion(prompt)
    if not response:
        return float('inf')  # Return infinity if there was an error in generation

    token_logprobs = response["choices"][0]["logprobs"]["token_logprobs"]

    nlls = [-100 if ll is None else ll for ll in token_logprobs]

    perplexity = math.exp(sum(nlls) / len(nlls))
    return perplexity
