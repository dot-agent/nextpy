# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import logging

from dotagent import compiler

from .config import Config


def get_product_list(relationship, age, occasion, interests, budget):
    llm = compiler.llms.OpenAI("text-davinci-003", token=Config.get_openai_key())
    
    # define the prompt
    gift_suggestions = compiler("""I'm looking for a gift, my relationship with the recipient is {{relationship}}. The recipient is {{age}} years old. The occasion is {{occasion}}. The recipient's interests and hobbies are {{interests}} I can give something related. My budget is {{budget}} dollars. Please suggest some gift ideas.
The following is a list of suggestions/keywords for locating products on Google in JSON format.
```json
{
    "gift_suggestions": [{{#geneach 'gift_suggestions'  num_iterations=10}} "{{gen 'this' temperature=1.0}}", {{~/geneach}}]
}```""", llm = llm)
    
    # generate the list of products
    result = gift_suggestions(relationship = relationship,age = age, occasion = occasion, interests = interests, budget = budget )
    logging.info(result)
    
    variables = result.variables().get('gift_suggestions', [])
    logging.info(variables)

    return variables

