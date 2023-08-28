import logging
import copy
import pdb
import math
import os
import json
import yaml
import time
import re
from typing import List, Dict

from factool.utils.base.pipeline import pipeline
from factool.code.helper.postprocess import PostProcessor
from factool.code.helper.execution import evaluate_test_cases_multi_solution
from factool.utils.utils_json import CustomJSONEncoder

class code_pipeline(pipeline):
    def __init__(self, foundation_model, multi_solution_cnt, testcases_input_cnt):
        super().__init__('code', foundation_model)

        self.multi_solution_cnt = multi_solution_cnt
        self.testcases_input_cnt = testcases_input_cnt

        with open(os.path.join(self.prompts_path, "query_generation.yaml"), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.query_generation_prompt = data['code']

    async def _testcases_input_generation(self, batch, testcases_input_cnt):
        messages_list = []
        if self.company == 'openai':
            messages_list = [
                [
                    {"role": "system", "content": self.query_generation_prompt['system']},
                    {"role": "user",
                     "content":
                         self.query_generation_prompt[
                             'user_testcases_' + str(testcases_input_cnt)
                             ].format(input_question=sample['prompt'],
                                      entry_point=sample['entry_point'])
                     },
                ]
                for sample in batch
            ]
        elif self.company == 'anthropic':
            messages_list = [self.query_generation_prompt[
                                 'user_testcases_' + str(testcases_input_cnt)
                                 ].format(input_question=sample['prompt'],
                                          entry_point=sample['entry_point'])
                             for sample in batch]
        return await self.chat.async_run(messages_list, Dict)
    
    async def _multi_solution_generation(self, batch, multi_solution_cnt):
        bsize = 15
        messages_list = [
            [
                {"role": "system", "content": self.query_generation_prompt['system']},
                {"role": "user", "content": self.query_generation_prompt[
                    'user_solutions'].format(input_question=sample['prompt'],
                                             entry_point=sample['entry_point'])},
            ]
            for sample in batch
        ]

        final_messages_list = [copy.deepcopy(messages)
                               for messages in messages_list
                               for _ in range(multi_solution_cnt)
                               ]

        responses = []
        for i in range(0, len(final_messages_list), bsize):
            batch = final_messages_list[i:i + bsize]
            responses += await self.chat.async_run(batch, Dict)
        
        # Split the list into lists of length of multi_solution_cnt
        responses_split = [responses[i:i + multi_solution_cnt]
                           for i in range(0, len(responses),
                                          multi_solution_cnt)]

        # Transform each element in each list
        multi_solutions = []
        for solutions in responses_split:
            key_names = [f"python_solution_{i}"
                         for i in range(1, multi_solution_cnt + 1)]
            new_element = {key: solutions[i]['python_solution']
            if solutions[i] != None else "None" for i, key in enumerate(key_names)}
            multi_solutions.append(new_element)

        return multi_solutions
    
    async def run_with_tool_live(self, batch, batch_size):
        testcases_input = await self._testcases_input_generation(batch, self.testcases_input_cnt)
        multi_solutions = await self._multi_solution_generation(batch, self.multi_solution_cnt)

        if testcases_input == None or multi_solutions == None:
            return None
        
        responses = []
        for i in range(batch_size):
            response = {'testcases_input': [],
                        'multi_solutions': [], 'with_tool_classification': "None"}
            try:
                response['testcases_input'] = list(testcases_input[i].values())
                # Append the solution to be verified to the LAST element
                # of multi_solutions
                response['multi_solutions']\
                    = [multi_solutions[i][f'python_solution_{j}']
                       for j in range(1, self.multi_solution_cnt + 1)] +\
                      [batch[i]['completion']]
            except:
                response['testcases_input'] = ["None"] * self.testcases_input_cnt
                response['multi_solutions'] = ["None"] * (self.multi_solution_cnt + 1)
            
            exec_result = evaluate_test_cases_multi_solution(
                batch[i]['prompt'], response['testcases_input'],
                response['multi_solutions'], timeout=0.1)
            response['exec_result'] = exec_result
            
            response['with_tool_classification'] = True
            # must pass all testcases to be classified as "True"
            for testcase_result in exec_result:
                # syntax or timeout error happening on the potential solution
                if isinstance(testcase_result[-1], str) \
                        and testcase_result[-1].startswith('FAILURE'):
                    response['with_tool_classification'] = False
                # majority voting. Note that the last element
                # is the solution to be verified. Also, multi solutions that return "FAILURE" are not counted and removed.
                else:
                    failure_indices = [
                        i for i, res in enumerate(testcase_result[:-1])
                        if isinstance(res, str) and res.startswith('FAILURE')]
                    testcase_result = [
                        res for i, res in enumerate(testcase_result)
                        if i not in failure_indices]

                    try:
                        if testcase_result[:-1].count(testcase_result[-1]) \
                                < math.ceil(len(testcase_result) / 2):
                            response['with_tool_classification'] = False
                    # sometimes numpy array is included in testcase_result, so this error will be raised
                    except:
                        response['with_tool_classification'] = False
            
            responses.append(response)

        return responses

    async def run_with_tool_api_call(self, prompts, responses, entry_points):

        # response preprocessing to extract the code snippet:
        claims = []
        for i, response in enumerate(responses):
            if "```python" in response:
                match = re.search(r"```python\n(.*?)\n```", response, re.DOTALL)
                if match:
                    claims.append(match.group(1))
                else:
                    claims.append("")
            elif "```" in response:
                match = re.search(r"```\n(.*?)\n```", response, re.DOTALL)
                if match:
                    claims.append(match.group(1))
                else:
                    claims.append("")
            else:
                claims.append(response)

        batch_size = 5
        num_batches = math.ceil(len(prompts) / batch_size)

        self.sample_list = [
            {"prompt": prompt, "response": response,
             "entry_point": entry_point, "completion": claim,
             "category": 'code'}
            for prompt, response, entry_point, claim
            in zip(prompts, responses, entry_points, claims)]

        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(responses))

            responses_returned = await self.run_with_tool_live(self.sample_list[batch_start: batch_end], batch_end - batch_start)

            for j, response_returned in enumerate(responses_returned):
                index = batch_start + j
                self.sample_list[index].update({
                    'claim': self.sample_list[index]['completion'],
                    'testcases_queries': response_returned['testcases_input'],
                    'potential_solutions_queries': response_returned['multi_solutions'],
                    'exec_results': response_returned['exec_result'],
                    'claim_level_factuality': response_returned['with_tool_classification'],
                    'response_level_factuality': response_returned['with_tool_classification']
                })
                del self.sample_list[index]["completion"]

        return self.sample_list
        
    async def run_with_tool_dataset(self, annotated_dataset_path: str, with_tool_classified_dataset_path: str, rerun: bool = False, rerun_indices: list = []):
        data_path = with_tool_classified_dataset_path if rerun else annotated_dataset_path
        with open(data_path, 'r') as f:
            data = [json.loads(line) for line in f]
        self.sample_list = data
        rerun_elements = self.sample_list if not rerun else [self.sample_list[i] for i in rerun_indices]

        batch_size = 5
        num_batches = math.ceil(len(rerun_elements) / batch_size) # 5

        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(rerun_elements))

            responses = await self.run_with_tool_live(rerun_elements[batch_start:batch_end], batch_end - batch_start)

            for j, response in enumerate(responses):
                index = batch_start + j if not rerun else rerun_indices[batch_start + j]
                self.sample_list[index]['with_tool_classification'] = response['with_tool_classification'] if response is not None else 'None'
                if response is not None:
                    self.sample_list[index].update({
                        'testcases_input': response['testcases_input'],
                        'multi_solutions': response['multi_solutions'],
                        'exec_result': response['exec_result']
                    })
        
            # save everything after each batch to prevent data loss
            with open(with_tool_classified_dataset_path, 'w') as f:
                for item in self.sample_list:
                    try:
                        json_str = json.dumps(item, cls=CustomJSONEncoder)
                    except:
                        continue
                    f.write(json_str + '\n')
    
    async def run_self_check_live(self, fewshot, batch):
        user_prompt_key = 'user_3_shot_CoT' if fewshot else 'user_zero_shot_CoT'
        messages_list = [
            [
                {"role": "system", "content": self.self_check_prompt['system']},
                {"role": "user", "content": self.self_check_prompt[user_prompt_key].format(input_question=response['prompt'], input_solution=response['completion'])},
            ]
            for response in batch
        ]
        return await self.chat.async_run(messages_list, Dict)

    async def run_self_check_dataset(self, annotated_dataset_path: str, self_check_classified_dataset_path: str, fewshot: bool = False, rerun: bool = False, rerun_indices: list = []):
        if rerun == False:
            with open(annotated_dataset_path, 'r') as f:
                self.sample_list = [json.loads(line) for line in f]
            rerun_elements = self.sample_list
        else:
            with open(self_check_classified_dataset_path, 'r') as f:
                self.sample_list = [json.loads(line) for line in f]
            rerun_elements = [self.sample_list[i] for i in rerun_indices]

        batch_size = 5
        num_batches = math.ceil(len(rerun_elements) / batch_size)

        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = (i + 1) * batch_size
            batch = rerun_elements[batch_start:batch_end]

            responses = await self.run_self_check_live(fewshot, batch)
            for j, response in enumerate(responses):
                index = batch_start + j if rerun == False else rerun_indices[batch_start + j]
                self.sample_list[index]['self_check_classification'] = response.get('factuality', 'None') if response is not None else 'None'
                self.sample_list[index]['self_check_reasoning'] = response.get('reasoning', 'None') if response is not None else 'None'
        
            # save everything after each batch to prevent data loss
            with open(self_check_classified_dataset_path, 'w') as f:
                for item in self.sample_list:
                    json_str = json.dumps(item)
                    f.write(json_str + '\n')