import json
import yaml
import os
import time
import math
import pdb
from typing import List, Dict

from openams.fact_check.knowledge_qa.tool import google_search
from openams.fact_check.knowledge_qa.tool import local_search
from openams.fact_check.utils.base.pipeline import pipeline

class knowledge_qa_pipeline(pipeline):
    def __init__(self, foundation_model, snippet_cnt, search_type, data_link=None, Embed_link=None):
        super().__init__('knowledge_qa', foundation_model)
        if(search_type == 'online'):
            self.tool = google_search(snippet_cnt = snippet_cnt)
        elif(search_type == 'local'):
            self.tool = local_search(snippet_cnt = snippet_cnt, data_link=data_link, embedding_link=Embed_link)
        with open(os.path.join(self.prompts_path, "claim_extraction.yaml"), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.claim_prompt = data['knowledge_qa']

        with open(os.path.join(self.prompts_path, 'query_generation.yaml'), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.query_prompt = data['knowledge_qa']

        with open(os.path.join(self.prompts_path, 'agreement_verification.yaml'), 'r') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
        self.verification_prompt = data['knowledge_qa']
    
    async def _claim_extraction(self, responses):
        messages_list = [
            [
                {"role": "system", "content": self.claim_prompt['system']},
                {"role": "user", "content": self.claim_prompt['user'].format(input=response)},
            ]
            for response in responses
        ]
        return await self.chat.async_run(messages_list, List)
    
    async def _query_generation(self, claims):
        if claims == None:
            return ['None']
        messages_list = [
            [
                {"role": "system", "content": self.query_prompt['system']},
                {"role": "user", "content": self.query_prompt['user'].format(input=claim['claim'] if 'claim' in claim else '')},
            ]
            for claim in claims
        ]
        return await self.chat.async_run(messages_list, List)

    async def _verification(self, claims, evidences):
        messages_list = [
            [
                {"role": "system", "content": self.verification_prompt['system']},
                {"role": "user", "content": self.verification_prompt['user'].format(claim=claim['claim'], evidence=str(evidence))},
            ]
            for claim, evidence in zip(claims, evidences)
        ]
        return await self.chat.async_run(messages_list, dict)
    
    async def run_with_tool_live(self, responses):
        claims_in_responses = await self._claim_extraction(responses)
        queries_in_responses = []
        evidences_in_responses = []
        sources_in_responses = []
        verifications_in_responses = []
        for claims_in_response in claims_in_responses:
            queries = await self._query_generation(claims_in_response)
            queries_in_responses.append(queries)
            search_outputs_for_claims = await self.tool.run(queries)
            evidences = [[output['content'] for output in search_outputs_for_claim] for search_outputs_for_claim in search_outputs_for_claims]
            evidences_in_responses.append(evidences)
            sources = [[output['source'] for output in search_outputs_for_claim] for search_outputs_for_claim in search_outputs_for_claims]
            sources_in_responses.append(sources)
            verifications = await self._verification(claims_in_response, evidences)
            verifications_in_responses.append(verifications)

        return claims_in_responses, queries_in_responses, evidences_in_responses, sources_in_responses, verifications_in_responses
    
    async def run_with_tool_live_without_claim_extraction(self, claims):
        queries = await self._query_generation(claims)
        evidences = await self.tool.run(queries)

        final_response = await self._verification(claims, evidences)
        for i in range(len(final_response)):
            if final_response[i] != None:
                final_response[i]['queries'] = queries[i]
                final_response[i]['evidences'] = evidences[i]

        return final_response
    
    async def run_with_tool_api_call(self, prompts, responses):
        batch_size = 5
        num_batches = math.ceil(len(prompts) / batch_size)

        self.sample_list = [{"prompt": prompt, "response": response, "category": 'kbqa'} for prompt, response in zip(prompts, responses)]

        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(responses))

            claims_in_responses, queries_in_responses, evidences_in_responses, sources_in_responses, verifications_in_responses = await self.run_with_tool_live(responses[batch_start:batch_end])

            for j, (claims_in_response, queries_in_response, evidences_in_response, sources_in_response, verifications_in_response) in enumerate(zip(claims_in_responses, queries_in_responses, evidences_in_responses, sources_in_responses, verifications_in_responses)):
                index = batch_start + j
                
                if claims_in_response != None:
                    for k, claim in enumerate(claims_in_response):
                        if verifications_in_response[k] != None:
                            if claim != None:
                                verifications_in_response[k].update({'claim': claim['claim']})
                            else:
                                verifications_in_response[k].update({'claim': 'None'})

                evidences_with_source = []
                for evidence, source in zip(evidences_in_response, sources_in_response):
                    evidences_with_source.append({'evidence': evidence, 'source': source})
                self.sample_list[index].update({
                    'claims': claims_in_response,
                    'queries': queries_in_response,
                    # 'evidences': evidences_in_response,
                    # 'sources': sources_in_response,
                    'evidences': evidences_with_source,
                    'claim_level_factuality': verifications_in_response,
                    'response_level_factuality': all([verification['factuality'] if verification != None else True for verification in verifications_in_response])
                })

        return self.sample_list
    
    async def run_with_tool_dataset(self, annotated_dataset_path: str, with_tool_classified_dataset_path: str, rerun: bool = False, rerun_indices: list = []):
        data_path = with_tool_classified_dataset_path if rerun else annotated_dataset_path
        with open(data_path, 'r') as f:
            data = [json.loads(line) for line in f]
        self.sample_list = data if rerun else [claim for sample in data for claim in sample['claims']]
        rerun_elements = self.sample_list if not rerun else [self.sample_list[i] for i in rerun_indices]

        batch_size = 4
        num_batches = math.ceil(len(rerun_elements) / batch_size) # 5
        
        for i in range(num_batches):
            print(i)
            batch_start = i * batch_size
            batch_end = min((i + 1) * batch_size, len(rerun_elements))

            responses = await self.run_with_tool_live_without_claim_extraction(rerun_elements[batch_start:batch_end])

            for j, response in enumerate(responses):
                index = batch_start + j if rerun == False else rerun_indices[batch_start + j]
                if response is None:
                    self.sample_list[index].update({
                        'with_tool_classification': 'None',
                        'with_tool_reasoning': 'None',
                        'queries': 'None',
                        'evidences': 'None'
                    })
                else:
                    self.sample_list[index].update({
                        'with_tool_classification': response.get('factuality', 'None'),
                        'with_tool_reasoning': response.get('reasoning', 'None'),
                        'queries': response.get('queries', 'None'),
                        'evidences': response.get('evidences', 'None')
                    })
        
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
                {"role": "user", "content": self.self_check_prompt[user_prompt_key].format(claim=response['claim'])},
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
