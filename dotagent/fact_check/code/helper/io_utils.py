# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import json

class Tools:
    @staticmethod
    def load_jsonl(file_path):
        json_objects = []
        with open(file_path, 'r', encoding='utf8') as f:
            for line in f:
                json_objects.append(json.loads(line.strip()))
        return json_objects
    
    @staticmethod
    def load_tasks(task_path):
        result = dict()
        lines = Tools.load_jsonl(task_path)
        for line in lines:
            result[line['task_id']] = line
        return result
        
    @staticmethod
    def write_file(path, content):
        with open(path, 'w', encoding='utf8') as f:
            f.write(content)