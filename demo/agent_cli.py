import sys
import os
from dotagent.agent.completion import TextCompletionAgent

# import environment variables
from dotenv import load_dotenv
load_dotenv()

# example of a prompt template 
prompt_template = '''
City: "{{city}}"
Average temperature (C): "{{gen 'avg_temp'}}"
Famous for (in 10 words): {{gen "famous_for" temperature=0.7 max_tokens=30}}'''

# example of a simple text completion agent
agent = TextCompletionAgent(
    prompt_template = prompt_template,
    return_complete=True,
    input_variables={'extras': ['city']}
    )

agent.cli_inputs()