'''
Will be removed before launching 
Env values will be passed from from os.environ
'''


import os
import yaml
from pathlib import Path


CONFIG_FILE = "config.yaml"
ROOT_DIR = os.path.dirname(Path(__file__).parent.parent)
config_path = ROOT_DIR + "/" + CONFIG_FILE

if os.path.exists(config_path):
    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file)

else:
    config_data = {'OPENAI_API_KEY': ""}
    config_data['OPENAI_API_KEY'] = input("Enter OPENAI_API_KEY:")
    config_data["OPENAI_ORG_ID"] = input("Enter OPENAI_ORG_ID:")
    config_data["SERP_API_KEY"] = input("Enter SERP_API_KEY:")
    config_data["GOOGLE_SEARCH_API_KEY"] = input("Enter GOOGLE_SEARCH_API_KEY:")


class Config:
    OPENAI_API_KEY = config_data["OPENAI_API_KEY"]
    OPENAI_ORG_ID = config_data["OPENAI_ORG_ID"]
    SERP_API_KEY = config_data["SERP_API_KEY"]
    GOOGLE_SEARCH_API_KEY = config_data["GOOGLE_SEARCH_API_KEY"]