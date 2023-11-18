import asyncio
import copy
import pdb

from openams.fact_check.knowledge_qa.pipeline import knowledge_qa_pipeline
from openams.fact_check.code.pipeline import code_pipeline
from openams.fact_check.math.pipeline import math_pipeline
from openams.fact_check.scientific.pipeline import scientific_pipeline
from openams.fact_check.med_doc_qa.pipeline import med_doc_qa_pipeline

class Factool():
    def __init__(self, foundation_model):
        self.foundation_model = foundation_model
        self.pipelines = {
                            "kbqa_online": knowledge_qa_pipeline(
                                foundation_model, 10, "online"
                            ),
                            "code": code_pipeline(
                                foundation_model, 3, 3
                            ),
                            "math": math_pipeline(
                                foundation_model
                            ),
                            "scientific": scientific_pipeline(
                                foundation_model
                            ),
                            "med_doc_qa": med_doc_qa_pipeline(
                                foundation_model
                            )
                        }

    def run(self, inputs):
        outputs = copy.deepcopy(inputs)
        batches = []
        current_category = inputs[0]['category']
        current_search_type = inputs[0].get('search_type', None)
        current_data_link = inputs[0].get('data_link', None)
        current_embedding_link = inputs[0].get('embedding_link', None)
        current_batch = []

        for input in inputs:
            if (input['category'] == current_category != 'kbqa') \
                or (input['category'] == current_category == 'kbqa' and input.get('search_type', None) == current_search_type == "online") \
                    or (input['category'] == current_category == 'kbqa' and input.get('search_type', None) == current_search_type == "local"\
                        and input.get('data_link', None)==current_data_link and input.get('embedding_link', None)==current_embedding_link):
                current_batch.append(input)
            else:
                batches.append(current_batch)
                current_batch = [input]
                current_category = input['category']
                current_search_type = input.get('search_type', None)
                current_data_link = input.get('data_link', None)
                current_embedding_link = input.get('embedding_link', None)
                    
        batches.append(current_batch)  # append the last batch

        index = 0
        for batch in batches:
            if not batch: continue
            category = batch[0]['category']
            search_type = batch[0].get('search_type', None)
            if category == 'code':
                batch_results = asyncio.run(
                    self.pipelines[category].run_with_tool_api_call(
                        [sample['prompt'] for sample in batch],
                        [sample['response'] for sample in batch],
                        [sample['entry_point'] for sample in batch]
                    )
                )
            elif category == 'kbqa':
                if search_type is None or search_type == "online":
                    batch_results = asyncio.run(
                        self.pipelines[category+"_online"].run_with_tool_api_call(
                            [sample['prompt'] for sample in batch],
                            [sample['response'] for sample in batch],
                        )
                    )
                else:
                    batch_results = asyncio.run(
                        knowledge_qa_pipeline(
                            self.foundation_model,2,"local",batch[0].get("data_link"),batch[0].get("embedding_link")
                        ).run_with_tool_api_call(
                            [sample['prompt'] for sample in batch],
                            [sample['response'] for sample in batch],
                        )
                    )
            else:
                batch_results = asyncio.run(
                    self.pipelines[category].run_with_tool_api_call(
                        [sample['prompt'] for sample in batch],
                        [sample['response'] for sample in batch]
                    )
                )
            for result in batch_results:
                outputs[index].update(result)
                index += 1
        
        # calculate average response_level_factuality
        total_response_factuality = sum(output['response_level_factuality'] == True for output in outputs)
        avg_response_level_factuality = total_response_factuality / len(outputs)

        # calculate average claim_level_factuality
        num_claims = 0
        total_claim_factuality = 0
        for output in outputs:
            num_claims += len(output['claim_level_factuality'])
            if output['category'] == 'kbqa':
                total_claim_factuality += sum(claim['factuality'] == True for claim in output['claim_level_factuality'])
            elif output['category'] == 'code':
                total_claim_factuality += (output['claim_level_factuality'] == True)
            elif output['category'] == 'math':
                total_claim_factuality += sum(claim_factuality == True for claim_factuality in output['claim_level_factuality'])
            elif output['category'] == 'scientific':
                total_claim_factuality += sum(claim['factuality'] == True for claim in output['claim_level_factuality'])

        avg_claim_level_factuality = total_claim_factuality / num_claims

        return {"average_claim_level_factuality": avg_claim_level_factuality, "average_response_level_factuality": avg_response_level_factuality, "detailed_information": outputs}

    async def run_for_plugin(self, inputs):
        outputs = copy.deepcopy(inputs)

        batches = []
        current_category = inputs[0]['category']
        current_batch = []

        for input in inputs:
            if input['category'] == current_category:
                current_batch.append(input)
            else:
                batches.append(current_batch)
                current_batch = [input]
                current_category = input['category']
                    
        batches.append(current_batch)  # append the last batch

        index = 0
        for batch in batches:
            category = batch[0]['category']
            if category == 'code':
                batch_results = await self.pipelines[category].run_with_tool_api_call(
                    [sample['prompt'] for sample in batch],
                    [sample['response'] for sample in batch],
                    [sample['entry_point'] for sample in batch],
                )
            else:
                batch_results = await self.pipelines[category].run_with_tool_api_call(
                    [sample['prompt'] for sample in batch],
                    [sample['response'] for sample in batch],
                )
            for result in batch_results:
                outputs[index].update(result)
                index += 1
        
        return outputs