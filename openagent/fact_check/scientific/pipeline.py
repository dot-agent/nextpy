import time
import json
import math
import os
import yaml
from typing import Dict, List

from factool.scientific.tool import google_scholar
from factool.utils.base.pipeline import pipeline

class scientific_pipeline(pipeline):
    def __init__(self, foundation_model):
        super().__init__('scientific', foundation_model)

        self.tool = google_scholar()

        with open(os.path.join(self.prompts_path, "claim_extraction.yaml"), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.claim_prompt = data['scientific']

        with open(os.path.join(self.prompts_path, 'agreement_verification.yaml'), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.verification_prompt = data['scientific']

    async def _claim_extraction(self, responses):
        messages_list = [
            [
                {"role": "system", "content": self.claim_prompt['system']},
                {"role": "user", "content": self.claim_prompt['user'].format(input=response)},
            ]
            for response in responses
        ]
        return await self.chat.async_run(messages_list, List)
    
    async def _check_authors(self, authors):
        messages_list = [
            [
                {"role": "system", "content": self.verification_prompt['system']},
                {"role": "user", "content": self.verification_prompt['user'].format(string1=claim_author, list2=real_author)},
            ]
            for claim_author, real_author in authors
        ]

        return await self.chat.async_run(messages_list, Dict)

    async def _verification(self, claims, responses):
        authors = [(claim['paper_author(s)'], response['author']) for claim, response in zip(claims, responses)]
        check_authors_results = await self._check_authors(authors)
        final_responses = []
        for i, (claim, response) in enumerate(zip(claims, responses)):
            final_response = {
                'generated_paper_title': claim['paper_title'],
                'generated_paper_author(s)': claim['paper_author(s)'],
                'generated_paper_pub_year': claim['paper_pub_year'],
                'actual_paper_title': response['title'],
                'actual_paper_author(s)': response['author'],
                'actual_paper_pub_year': response['pub_year'],
            }

            errors = []
            if final_response['generated_paper_title'].lower() != final_response['actual_paper_title'].lower() and final_response['generated_paper_title'].lower() not in final_response['actual_paper_title'].lower() and final_response['actual_paper_title'].lower() not in final_response['generated_paper_title'].lower() :
                errors.append('wrong_paper_title')
            if check_authors_results[i]['factuality'] == False:
                errors.append('wrong_paper_author(s)')
            if final_response['generated_paper_pub_year'] != final_response['actual_paper_pub_year']:
                errors.append('wrong_paper_pub_year')

            final_response['error'] = errors
            final_response['factuality'] = len(errors) == 0

            final_responses.append(final_response)

        return final_responses

    async def run_with_tool_live(self, samples):
        claims_in_responses = await self._claim_extraction(samples)
        queries_in_responses = []
        evidences_in_responses = []
        verifications_in_responses = []
        for claims_in_response in claims_in_responses:
            queries = [claim['paper_title'] for claim in claims_in_response]
            queries_in_responses.append(queries)
            evidences = [self.tool.run(paper_title) for paper_title in queries]
            evidences_in_responses.append(evidences)
            verifications = await self._verification(claims_in_response, evidences)
            verifications_in_responses.append(verifications)

        return claims_in_responses, queries_in_responses, evidences_in_responses, verifications_in_responses
        
    async def run_with_tool_live_without_claim_extraction(self, claims):
        # claims = [{"paper_title": "A Survey of Modern Authorship Attribution Methods", "paper_author(s)": "Stamatatos, Efstathios", "paper_pub_year": "2013"}, {"paper_title": "BERT", "paper_author(s)": "John Smith", "paper_pub_year": "2020"}]
        papers_titles = [claim['paper_title'] for claim in claims]
        responses = [self.tool.run(paper_title) for paper_title in papers_titles]
        final_response = await self._verification(claims, responses)
        return final_response

    async def run_with_tool_api_call(self, prompts, responses):
        batch_size = 5
        num_batches = math.ceil(len(prompts) / batch_size)

        self.sample_list = [{"prompt": prompt, "response": response, "category": 'scientific'} for prompt, response in zip(prompts, responses)]

        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(responses))

            claims_in_responses, queries_in_responses, evidences_in_responses, verifications_in_responses = await self.run_with_tool_live(responses[batch_start:batch_end])

            for j, (claims_in_response, queries_in_response, evidences_in_response, verifications_in_response) in enumerate(zip(claims_in_responses, queries_in_responses, evidences_in_responses, verifications_in_responses)):
                index = batch_start + j

                self.sample_list[index].update({
                    'claims': claims_in_response,
                    'queries': queries_in_response,
                    'evidences': evidences_in_response,
                    'claim_level_factuality': verifications_in_response,
                    'response_level_factuality': all([verification['factuality'] if verification != None else True for verification in verifications_in_response])
                })
        return self.sample_list

    async def run_with_tool_dataset(self, annotated_dataset_path: str, with_tool_classified_dataset_path: str, rerun: bool = False, rerun_indices: list = []):
        # Example of a line: 
        # {"paper_title": "A Survey of Modern Authorship Attribution Methods", "paper_author(s)": "Stamatatos, Efstathios", "paper_pub_year": "2013", "label": True / False}
        if rerun == False:
            with open(annotated_dataset_path, 'r') as f:
                data = [json.loads(line) for line in f]
            self.sample_list = [claim for sample in data for claim in sample['claims']]
            rerun_elements = self.sample_list
        else:
            with open(with_tool_classified_dataset_path, 'r') as f:
                data = [json.loads(line) for line in f]
            self.sample_list = data
            rerun_elements = [self.sample_list[i] for i in rerun_indices]

        batch_size = 5
        num_batches = math.ceil(len(rerun_elements) / batch_size) # 5

        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = (i + 1) * batch_size if (i + 1) * batch_size < len(rerun_elements) else len(rerun_elements)

            responses = await self.run_with_tool_live_without_claim_extraction(rerun_elements[batch_start:batch_end])
            for j, response in enumerate(responses):
                index = batch_start + j if rerun == False else rerun_indices[batch_start + j]
                if response == None:
                    self.sample_list[index]['with_tool_classification'] = 'None'
                    self.sample_list[index]['error'] = 'None'
                else:
                    self.sample_list[index]['with_tool_classification'] = response.get('factuality', 'None')
                    self.sample_list[index]['error'] = response.get('error', 'None')
        
            # save everything after each batch to prevent data loss
            with open(with_tool_classified_dataset_path, 'w') as f:
                for item in self.sample_list:
                    json_str = json.dumps(item)
                    f.write(json_str + '\n')

    async def run_self_check_live(self, fewshot, batch):
        user_prompt_key = 'user_3_shot_CoT' if fewshot else 'user_zero_shot_CoT'
        messages_list = [
            [
                {"role": "system", "content": self.self_check_prompt['system']},
                {"role": "user", "content": self.self_check_prompt[user_prompt_key].format(scientific_literature=response)}
            ]
            for response in batch
        ]
        return await self.chat.async_run(messages_list, Dict)

    async def run_self_check_dataset(self, annotated_dataset_path: str, self_check_classified_dataset_path: str, fewshot: bool = False, rerun: bool = False, rerun_indices: list = []):
        # Example of a line: 
        # {"paper_title": "A Survey of Modern Authorship Attribution Methods", "paper_author(s)": "Stamatatos, Efstathios", "paper_pub_year": "2013", "annotation": True / False}
        data_path = annotated_dataset_path if not rerun else self_check_classified_dataset_path
        with open(data_path, 'r') as f:
            data = [json.loads(line) for line in f]
        self.sample_list = data if rerun else [claim for sample in data for claim in sample['claims']]
        rerun_elements = self.sample_list if not rerun else [self.sample_list[i] for i in rerun_indices]

        batch_size = 5
        num_batches = math.ceil(len(rerun_elements) / batch_size)

        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = (i + 1) * batch_size
            batch = rerun_elements[batch_start:batch_end]
            batch = [{k:v for k,v in d.items() if k != "label"} for d in batch]

            responses = await self.run_self_check_live(fewshot, batch)
            for j, response in enumerate(responses):
                index = batch_start + j if rerun == False else rerun_indices[batch_start + j]
                if response == None:
                    self.sample_list[index]['self_check_classification'] = 'None'
                    self.sample_list[index]['self_check_reasoning'] = 'None'
                else:
                    self.sample_list[index]['self_check_classification'] = response.get('factuality', 'None')
                    self.sample_list[index]['self_check_reasoning'] = response.get('reasoning', 'None')
        
            # save everything after each batch to prevent data loss
            with open(self_check_classified_dataset_path, 'w') as f:
                for item in self.sample_list:
                    json_str = json.dumps(item)
                    f.write(json_str + '\n')