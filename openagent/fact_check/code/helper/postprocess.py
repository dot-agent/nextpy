# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

from collections import defaultdict

from factool.code.helper.io_utils import Tools

STOP_TOKEN = ['\nclass', '\ndef', '\n#', '\nif', '\nprint']

class PostProcessor:
    @staticmethod
    def map_task_id_for_solution(predict_path, source_path):
        database = dict()
        raw_problems = Tools.load_tasks(source_path)
        for task_id in raw_problems.keys():
            database[raw_problems[task_id]['prompt']] = raw_problems[task_id]

        result = []
        predictions = Tools.load_jsonl(predict_path)
        
        for pre in predictions:
            task = database[pre['prompt']]
            
            for sample in pre['samples']:
                processed_code = PostProcessor.solution_extract(sample)
                result.append({
                    'task_id': task['task_id'],
                    'prompt': pre['prompt'],
                    'test': task['test'],
                    'entry_point': task['entry_point'],
                    'completion': processed_code
                })
        return result, len(raw_problems)

    @staticmethod
    def solution_extract(content):
        for identifier in STOP_TOKEN:
            if identifier in content:
                content = content.split(identifier)[0]
        return content