from typing import Any, Dict, List, Optional
from pydantic import BaseModel, root_validator
from nextpy.ai.models.embedding.base import Embeddings
from nextpy.utils.data_ops import get_from_dict_or_env


class AlephAlphaAsymmetricSemanticEmbedding(BaseModel, Embeddings):

    client: Any  #: :meta private:

    model: Optional[str] = "luminous-base"
    hosting: Optional[str] = "https://api.aleph-alpha.com"
    normalize: Optional[bool] = True
    compress_to_size: Optional[int] = 128
    contextual_control_threshold: Optional[int] = None
    control_log_additive: Optional[bool] = True
    aleph_alpha_api_key: Optional[str] = None

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        aleph_alpha_api_key = get_from_dict_or_env(
            values, "aleph_alpha_api_key", "ALEPH_ALPHA_API_KEY"
        )
        try:
            from aleph_alpha_client import Client
        except ImportError:
            raise ValueError(
                "Could not import aleph_alpha_client python package. "
                "Please install it with `pip install aleph_alpha_client`."
            )
        values["client"] = Client(token=aleph_alpha_api_key)
        return values

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Call out to Aleph Alpha's asymmetric Document endpoint.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        try:
            from aleph_alpha_client import (
                Prompt,
                SemanticEmbeddingRequest,
                SemanticRepresentation,
            )
        except ImportError:
            raise ValueError(
                "Could not import aleph_alpha_client python package. "
                "Please install it with `pip install aleph_alpha_client`."
            )
        document_embeddings = []

        for text in texts:
            document_params = {
                "prompt": Prompt.from_text(text),
                "representation": SemanticRepresentation.Document,
                "compress_to_size": self.compress_to_size,
                "normalize": self.normalize,
                "contextual_control_threshold": self.contextual_control_threshold,
                "control_log_additive": self.control_log_additive,
            }

            document_request = SemanticEmbeddingRequest(**document_params)
            document_response = self.client.semantic_embed(
                request=document_request, model=self.model
            )

            document_embeddings.append(document_response.embedding)

        return document_embeddings

    def embed_query(self, text: str) -> List[float]:
        """Call out to Aleph Alpha's asymmetric, query embedding endpoint
        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        try:
            from aleph_alpha_client import (
                Prompt,
                SemanticEmbeddingRequest,
                SemanticRepresentation,
            )
        except ImportError:
            raise ValueError(
                "Could not import aleph_alpha_client python package. "
                "Please install it with `pip install aleph_alpha_client`."
            )
        symmetric_params = {
            "prompt": Prompt.from_text(text),
            "representation": SemanticRepresentation.Query,
            "compress_to_size": self.compress_to_size,
            "normalize": self.normalize,
            "contextual_control_threshold": self.contextual_control_threshold,
            "control_log_additive": self.control_log_additive,
        }

        symmetric_request = SemanticEmbeddingRequest(**symmetric_params)
        symmetric_response = self.client.semantic_embed(
            request=symmetric_request, model=self.model
        )

        return symmetric_response.embedding


class AlephAlphaSymmetricSemanticEmbedding(AlephAlphaAsymmetricSemanticEmbedding):
    """The symmetric version of the Aleph Alpha's semantic embeddings.

    The main difference is that here, both the documents and
    queries are embedded with a SemanticRepresentation.Symmetric
    Example:
        .. code-block:: python

            from aleph_alpha import AlephAlphaSymmetricSemanticEmbedding

            embeddings = AlephAlphaAsymmetricSemanticEmbedding()
            text = "This is a test text"

            doc_result = embeddings.embed_documents([text])
            query_result = embeddings.embed_query(text)
    """

    def _embed(self, text: str) -> List[float]:
        try:
            from aleph_alpha_client import (
                Prompt,
                SemanticEmbeddingRequest,
                SemanticRepresentation,
            )
        except ImportError:
            raise ValueError(
                "Could not import aleph_alpha_client python package. "
                "Please install it with `pip install aleph_alpha_client`."
            )
        query_params = {
            "prompt": Prompt.from_text(text),
            "representation": SemanticRepresentation.Symmetric,
            "compress_to_size": self.compress_to_size,
            "normalize": self.normalize,
            "contextual_control_threshold": self.contextual_control_threshold,
            "control_log_additive": self.control_log_additive,
        }

        query_request = SemanticEmbeddingRequest(**query_params)
        query_response = self.client.semantic_embed(
            request=query_request, model=self.model
        )

        return query_response.embedding

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Call out to Aleph Alpha's Document endpoint.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        document_embeddings = []

        for text in texts:
            document_embeddings.append(self._embed(text))
        return document_embeddings

    def embed_query(self, text: str) -> List[float]:
        """Call out to Aleph Alpha's asymmetric, query embedding endpoint
        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        return self._embed(text)
