from typing import List

from openagent.schema import BaseRetriever, Document
from openagent.knowledgebase.utilities.arxiv import ArxivAPIWrapper


class ArxivRetriever(BaseRetriever, ArxivAPIWrapper):
    """
    It is effectively a wrapper for ArxivAPIWrapper.
    It wraps load() to get_relevant_documents().
    It uses all ArxivAPIWrapper arguments without any change.
    """

    def get_relevant_documents(self, query: str) -> List[Document]:
        return self.load(query=query)

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        raise NotImplementedError("ArxivRetriver does not support async")