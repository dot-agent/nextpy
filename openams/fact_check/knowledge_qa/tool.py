import asyncio
from openams.fact_check.knowledge_qa.google_serper import GoogleSerperAPIWrapper
from openams.fact_check.utils.openai_wrapper import OpenAIEmbed
import json
import os
import numpy as np
import jsonlines
import pdb

class google_search():
    def __init__(self, snippet_cnt):
        self.serper = GoogleSerperAPIWrapper(snippet_cnt=snippet_cnt)

    async def run(self, queries):
        return await self.serper.run(queries)

class local_search():
    def __init__(self, snippet_cnt, data_link, embedding_link=None):
        self.snippet_cnt = snippet_cnt
        self.data_link = data_link
        self.embedding_link = embedding_link
        self.openai_embed = OpenAIEmbed()
        self.data = None
        self.embedding = None
        asyncio.run(self.init_async())
        
    
    async def init_async(self):
        print("init local search")
        self.load_data_by_link()
        if self.embedding_link is None:
            await self.calculate_embedding()
        else:
            self.load_embedding_by_link()
        print("loaded data and embedding")

    def add_suffix_to_json_filename(self, filename):
        base_name, extension = os.path.splitext(filename)
        return base_name + '_embed' + extension

    def load_data_by_link(self):
        #load data from json link
        self.data = []
        #self.data = json.load(open(self.data_link, 'r'))
        with jsonlines.open(self.data_link) as reader:
            for obj in reader:
                self.data.append(obj['text'])

    def load_embedding_by_link(self):
        self.embedding = []
        #self.embedding = json.load(open(self.embedding_link, 'r'))
        with jsonlines.open(self.embedding_link) as reader:
            for obj in reader:
                self.embedding.append(obj)
    
    def save_embeddings(self):
        #json.dump(self.embedding, open(self.add_suffix_to_json_filename(self.data_link), 'w'))
        with jsonlines.open(self.add_suffix_to_json_filename(self.data_link), mode='w') as writer:
            writer.write_all(self.embedding)

    async def calculate_embedding(self):
        result = await self.openai_embed.process_batch(self.data,retry=3)
        self.embedding = [emb["data"][0]["embedding"] for emb in result]
        self.save_embeddings()

    async def search(self, query):
        result = await self.openai_embed.create_embedding(query)
        query_embed = result["data"][0]["embedding"]
        dot_product = np.dot(self.embedding, query_embed)
        sorted_indices = np.argsort(dot_product)[::-1]
        top_k_indices = sorted_indices[:self.snippet_cnt]
        return [{"content":self.data[i],"source":"local"} for i in top_k_indices]

    
    async def run(self, queries):
        flattened_queries = []
        for sublist in queries:
            if sublist is None:
                sublist = ['None', 'None']
            for item in sublist:
                flattened_queries.append(item)
        
        snippets = await asyncio.gather(*[self.search(query) for query in flattened_queries])
        snippets_split = [snippets[i] + snippets[i+1] for i in range(0, len(snippets), 2)]
        return snippets_split






