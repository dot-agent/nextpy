from typing import List

import numpy as np
from pydantic import BaseModel

from nextpy.ai.models.embedding.base import Embeddings


class FakeEmbeddings(Embeddings, BaseModel):
    size: int

    def _get_embedding(self) -> List[float]:
        return list(np.random.normal(size=self.size))

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._get_embedding() for _ in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._get_embedding()
