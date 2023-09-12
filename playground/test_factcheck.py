import sys
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
dotagent_dir = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(dotagent_dir)

from dotagent.llms._openai import OpenAI
from dotagent.fact_check.factool import Factool
from dotenv import load_dotenv

load_dotenv()

# Initialize a Factool instance with the specified keys. foundation_model could be either "gpt-3.5-turbo" or "gpt-4"
factool_instance = Factool("gpt-4")

inputs = [
            {
                "prompt": "Introduce Graham Neubig",
                "response": "Graham Neubig is a professor at MIT",
                "category": "kbqa"
            },
]
response_list = factool_instance.run(inputs)

print(response_list)