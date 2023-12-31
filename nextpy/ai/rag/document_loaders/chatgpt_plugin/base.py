# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""ChatGPT Plugin."""

import os
from typing import Any, List, Optional

import requests
from requests.adapters import HTTPAdapter, Retry

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class ChatGPTRetrievalPluginReader(BaseReader):
    """ChatGPT Retrieval Plugin reader."""

    def __init__(
        self,
        endpoint_url: str,
        bearer_token: Optional[str] = None,
        retries: Optional[Retry] = None,
        batch_size: int = 100,
    ) -> None:
        """Chatgpt Retrieval Plugin."""
        self._endpoint_url = endpoint_url
        self._bearer_token = bearer_token or os.getenv("BEARER_TOKEN")
        self._retries = retries
        self._batch_size = batch_size

        self._s = requests.Session()
        self._s.mount("http://", HTTPAdapter(max_retries=self._retries))

    def load_data(
        self,
        query: str,
        top_k: int = 10,
        separate_documents: bool = True,
        **kwargs: Any,
    ) -> List[DocumentNode]:
        """Load data from ChatGPT Retrieval Plugin."""
        headers = {"Authorization": f"Bearer {self._bearer_token}"}
        queries = [{"query": query, "top_k": top_k}]
        res = requests.post(
            f"{self._endpoint_url}/query", headers=headers, json={"queries": queries}
        )

        metadata = {
            "endpoint_url": self._endpoint_url,
            "query": query,
            "tok_k": top_k,
            "separate_documents": separate_documents,
        }
        documents: List[DocumentNode] = []
        for query_result in res.json()["results"]:
            for result in query_result["results"]:
                result_id = result["id"]
                result_txt = result["text"]
                result_embedding = result["embedding"]
                doc = DocumentNode(
                    text=result_txt,
                    doc_id=result_id,
                    embedding=result_embedding,
                    extra_info=metadata,
                )
                documents.append(doc)

            # NOTE: there should only be one query
            break

        if not separate_documents:
            text_list = [doc.get_text() for doc in documents]
            text = "\n\n".join(text_list)
            documents = [DocumentNode(text=text, extra_info=metadata)]

        return documents
