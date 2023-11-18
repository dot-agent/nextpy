import openai
import math
from openams.utils import get_from_dict_or_env
def gen_openai_completion(prompt: str):
  openai_api_key = get_from_dict_or_env("OPENAI_API_KEY")
  openai.api_key = openai_api_key
  #GET THE LOGPROB OF THE PROMPT
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=prompt,
    max_tokens=0,
    echo=True,
    logprobs=0
  )
  return response["choices"][0]["logprobs"]["token_logprobs"]

def calculate_perplexity(prompt: str):
  nlls = []

  token_logprobs = gen_openai_completion(prompt)
  for neg_log_likelihood in token_logprobs:
    if neg_log_likelihood == None: #default to -100, handles the initial token case
      neg_log_likelihood = -100
    nlls.append(neg_log_likelihood)

  perplexity = math.exp(sum(nlls)/len(token_logprobs))
  return perplexity