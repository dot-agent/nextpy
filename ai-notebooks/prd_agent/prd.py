# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.


import os
from pathlib import Path

import pkg_resources as pg
from dotenv import load_dotenv

from nextpy.ai import engine


def load_environment_variables():
    load_dotenv()
    return {
        "openai_api_key": os.getenv("OPENAI_API_KEY")
    }

# Initialize the OpenAI client with the API key
env_vars = load_environment_variables()
api_key=env_vars["openai_api_key"] = 'sk-enter-api-key'


llm = engine.llms.OpenAI("gpt-3.5-turbo", chat_mode=True, api_key=api_key, caching=False)


path = pg.resource_filename(__name__, 'prompts/prd.hbs')
prd_prompt_template = Path(path).read_text()

path = pg.resource_filename(__name__, 'prompts/prompt.hbs')
prompt_template = Path(path).read_text()

# prompt_template.format(FORMAT_EXAMPLE)


engine = engine(template = prompt_template, llm = llm, silent=True)

class PRDDeveloper:
    def __init__(self, goal = None, prd_prompt_template = prd_prompt_template, engine = engine
                ):

        self.goal = goal
        self.prd_prompt_template = prd_prompt_template
        self.engine = engine

    def run(self):
        output = self.engine(goal = self.goal, prompt_template = self.prd_prompt_template, llm=llm)
        return output['response']

        
