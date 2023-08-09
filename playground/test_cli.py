import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
openagent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(openagent_dir)


from openagent.agent.completion import TextCompletionAgent

from dotenv import load_dotenv
load_dotenv()

text_template = '''
City: "{{city}}"
Average temperature (C): "{{gen 'avg_temp'}}"
Population: "{{population}}"
Famous for (in 10 words): {{gen "famous_for" temperature=0.7 max_tokens=30}}'''

agent = TextCompletionAgent(
    prompt_template = text_template,
    return_complete=True,
    input_variables={'extras': ['city', 'population']}
    )

agent.cli()

# agent.cli_gptengg()