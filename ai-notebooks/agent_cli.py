# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

# import environment variables
from dotenv import load_dotenv

from nextpy.ai.agent.completion import TextCompletionAgent

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
