import os
import pathlib
import openai
import yaml
import json
import asyncio
from tqdm import tqdm
from openams.fact_check.env_config import factool_env_config


# env
# openai.api_key = factool_env_config.openai_api_key


config = {
    'model_name': 'gpt-3.5-turbo',
    'max_tokens': 2000,
    'temperature': 0.0,
    'top_p': 1,
    'frequency_penalty': 0.0,
    'presence_penalty': 0.0,
    'n': 1
}


# Make api calls asynchronously
async def run_api(messages):
    async def single_run(message):
        output = openai.ChatCompletion.create(
            model=config['model_name'],
            messages=message,
            max_tokens=config['max_tokens'],
            temperature=config['temperature'],
            top_p=config['top_p'],
            frequency_penalty=config['frequency_penalty'],
            presence_penalty=config['presence_penalty'],
            n=config['n'],
        )
        return output.choices[0].message.content.strip()

    responses = [single_run(messages[index]) for index in range(len(messages))]
    return await asyncio.gather(*responses)



# Import data from scientific.json
scientific_list = []
with open("../datasets/scientific/scientific.json", "r") as f:
    data = json.load(f)
    for dict_data in data:
        cur_dict = {'dataset_name': 'scientific',
                    'question': dict_data["question"],
                    'factual_response': dict_data['factual_response']}
        scientific_list.append(cur_dict)

# Apply template prompt
with open("./prompts/claim_extraction.yaml") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
prompt = data['scientific']
messages_list = [
    [
        {"role": "system", "content": prompt['system']},
        {"role": "user", "content": prompt['user'].format(input=sample['factual_response'])},
    ]
    for sample in scientific_list
]

assert len(messages_list) == len(scientific_list), "The data length is different"

# Run the API to get the output
print("begin claims extraction...")
results = asyncio.run(run_api(messages_list))
for i in range(len(scientific_list)):
    scientific_list[i]["claims"] = results[i]

with open('../datasets/scientific/scientific_claims.json', 'w') as f:
    json.dump(scientific_list, f, indent=4)


"""
The scientific_claims.json file saved by the above code may have format problems, here are some adjustments
"""
with open("../datasets/scientific/scientific_claims.json", "r") as f:
    data = json.load(f)
    for data_i in tqdm(data, total=len(data)):
        try:
            data_i["claims"] = json.loads(data_i["claims"].strip())
        except:
            print(data_i["claims"])
            continue
with open("../datasets/scientific/scientific_claims.json", "w") as f:
    json.dump(data, f, indent=4)
