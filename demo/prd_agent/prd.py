
from typing import List, Tuple
from openams import engine
from openams.endpoints._openai import OpenAI
import pkg_resources as pg
from pathlib import Path


path = pg.resource_filename(__name__, 'prompts/prd.hbs')
prd_prompt_template = Path(path).read_text()

path = pg.resource_filename(__name__, 'prompts/prompt.hbs')
prompt_template = Path(path).read_text()

# prompt_template.format(FORMAT_EXAMPLE)
llm = OpenAI("gpt-4")

engine = engine(template = prompt_template, llm = llm, silent=True)

class PRDDeveloper:
    def __init__(self, goal = None, prd_prompt_template = prd_prompt_template, engine = engine
                ):

        self.goal = goal
        self.prd_prompt_template = prd_prompt_template
        self.engine = engine

    def run(self):
        output = self.engine(goal = self.goal, prompt_template = self.prd_prompt_template)
        return output['response']

        
