import json
import math
import os
from typing import List, Dict
import yaml
import pdb

from factool.math.tool import python_executor
from factool.utils.base.pipeline import pipeline

class math_pipeline(pipeline):
    def __init__(self, foundation_model):
        super().__init__('math', foundation_model)

        self.tool = python_executor()

        with open(os.path.join(self.prompts_path, "claim_extraction.yaml"), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.claim_prompt = data['math']

        with open(os.path.join(self.prompts_path, 'query_generation.yaml'), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.query_prompt = data['math']

    def _verification(self, exec_results):
        classification_results = [True for _ in range(len(exec_results))]
        for i in range(len(exec_results)):
            if exec_results[i] is not None and 'False' in exec_results[i]:
                classification_results[i] = False
        
        return classification_results

    async def _claim_extraction(self, samples):
        messages_list = [
            [
                {"role": "system", "content": self.claim_prompt['system']},
                {"role": "user", "content": self.claim_prompt['user'].format(input_question=sample['prompt'], input_solution=sample['response'])},
            ]
            for sample in samples
        ]
        return await self.chat.async_run(messages_list, List)
    
    async def _query_generation(self, claims):
        messages_list = [
            [
                {"role": "system", "content": self.query_prompt['system']},
                {"role": "user", "content": self.query_prompt['user'].format(math_calculation=claim['math_calculation'], calculated_answer=claim['calculated_answer'])},
            ]
            for claim in claims
        ]
        return await self.chat.async_run(messages_list, Dict)
    
    async def run_with_tool_live(self, samples):
        claims_in_responses = await self._claim_extraction(samples)
        queries_in_responses = []
        exec_results_in_responses = []
        verifications_in_responses = []
        for claims_in_response in claims_in_responses:
            queries = await self._query_generation(claims_in_response)
            queries_in_responses.append(queries)
            exec_results = []
            for query in queries:
                try:
                    exec_results.append(self.tool.run(query['python_snippet']))
                except:
                    exec_results.append('None')
            exec_results_in_responses.append(exec_results)
            verifications = self._verification(exec_results)
            verifications_in_responses.append(verifications)

        return claims_in_responses, queries_in_responses, exec_results_in_responses, verifications_in_responses
    
    async def run_with_tool_live_without_claim_extraction(self, claims):
        queries = await self._query_generation(claims)

        exec_results = []
        for query in queries:
            try:
                exec_results.append(self.tool.run(query['python_snippet']))
            except:
                exec_results.append(None)
        classification_results = self._verification(exec_results)
        return queries, exec_results, classification_results
    
    async def run_with_tool_api_call(self, prompts, responses):
        batch_size = 5
        num_batches = math.ceil(len(prompts) / batch_size)

        self.sample_list = [{"prompt": prompt, "response": response, "category": 'math'} for prompt, response in zip(prompts, responses)]

        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(responses))

            claims_in_responses, queries_in_responses, exec_results_in_response, verifications_in_responses = await self.run_with_tool_live(self.sample_list[batch_start: batch_end])

            for j, (claims_in_response, queries_in_response, exec_results_in_response, verifications_in_response) in enumerate(zip(claims_in_responses, queries_in_responses, exec_results_in_response, verifications_in_responses)):
                index = batch_start + j

                self.sample_list[index].update({
                    'claims': claims_in_response,
                    'queries': queries_in_response,
                    'execution_results': exec_results_in_response,
                    'claim_level_factuality': verifications_in_response,
                    'response_level_factuality': all([verification if verification != None else True for verification in verifications_in_response])
                })

        return self.sample_list

    async def run_with_tool_dataset(self, annotated_dataset_path: str, with_tool_classified_dataset_path: str, rerun: bool = False, rerun_indices: list = []):
        data_path = annotated_dataset_path if not rerun else with_tool_classified_dataset_path
        with open(data_path, 'r') as f:
            data = [json.loads(line) for line in f]
        self.sample_list = data if rerun else [claim for sample in data for claim in sample['claims']]
        rerun_elements = self.sample_list if not rerun else [self.sample_list[i] for i in rerun_indices]

        batch_size = 10
        num_batches = math.ceil(len(rerun_elements) / batch_size) # 5

        for i in range(num_batches):
            print("test1")
            print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(rerun_elements))
            batch = rerun_elements[batch_start:batch_end]

            queries, exec_results, classification_results = await self.run_with_tool_live_without_claim_extraction(batch)

            for j, (query, exec_result, classification_result) in enumerate(zip(queries, exec_results, classification_results)):
                index = batch_start + j if not rerun else rerun_indices[batch_start + j]
                self.sample_list[index].update({
                    'query': query,
                    'exec_result': exec_result,
                    'with_tool_classification': classification_result,
                })
        
            # save everything after each batch to prevent data loss
            with open(with_tool_classified_dataset_path, 'w') as f:
                for item in self.sample_list:
                    try:
                        json_str = json.dumps(item)
                    except:
                        continue
                    f.write(json_str + '\n')

    async def run_self_check_live(self, fewshot, batch):
        user_prompt_key = 'user_3_shot_CoT' if fewshot else 'user_zero_shot_CoT'
        messages_list = [
            [
                {"role": "system", "content": self.self_check_prompt['system']},
                {"role": "user", "content": self.self_check_prompt[user_prompt_key].format(input_calculation=response['math_calculation'], input_calculated_answer=response['calculated_answer'])},
            ]
            for response in batch
        ]
        return await self.chat.async_run(messages_list, Dict)

    async def run_self_check_dataset(self, annotated_dataset_path: str, self_check_classified_dataset_path: str, fewshot: bool = False, rerun: bool = False, rerun_indices: list = []):
        data_path = annotated_dataset_path if not rerun else self_check_classified_dataset_path
        with open(data_path, 'r') as f:
            data = [json.loads(line) for line in f]
        self.sample_list = data if rerun else [claim for sample in data for claim in sample['claims']]
        rerun_elements = self.sample_list if not rerun else [self.sample_list[i] for i in rerun_indices]

        batch_size = 10
        num_batches = math.ceil(len(rerun_elements) / batch_size)

        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(rerun_elements))
            batch = rerun_elements[batch_start:batch_end]

            responses = await self.run_self_check_live(fewshot, batch)
            for j, response in enumerate(responses):
                index = batch_start + j if not rerun else rerun_indices[batch_start + j]
                if response is None:
                    self.sample_list[index].update({
                        'self_check_classification': 'None',
                        'self_check_reasoning': 'None'
                    })
                else:
                    self.sample_list[index].update({
                        'self_check_classification': response.get('factuality', 'None'),
                        'self_check_reasoning': response.get('reasoning', 'None')
                    })

            # save everything after each batch to prevent data loss
            with open(self_check_classified_dataset_path, 'w') as f:
                for item in self.sample_list:
                    json_str = json.dumps(item)
                    f.write(json_str + '\n')