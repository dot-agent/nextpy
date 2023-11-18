"""Wrapper around HuggingFace embedding models: hub, sentence-transformers and instruct embeddings"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, root_validator, Field

from openams.rag.vectordb.embeddings.base import Embeddings
from openams.utils import get_from_dict_or_env


DEFAULT_MODEL_NAME = "sentence-transformers/all-mpnet-base-v2"
DEFAULT_INSTRUCT_MODEL = "hkunlp/instructor-large"
DEFAULT_EMBED_INSTRUCTION = "Represent the document for retrieval: "
DEFAULT_QUERY_INSTRUCTION = (
    "Represent the question for retrieving supporting documents: "
)

DEFAULT_REPO_ID = "sentence-transformers/all-mpnet-base-v2"
VALID_TASKS = ("feature-extraction",)


class HuggingFaceHubEmbeddings(BaseModel, Embeddings):
    """Wrapper around HuggingFaceHub embedding models.

    To use, you should have the ``huggingface_hub`` python package installed, and the
    environment variable ``HUGGINGFACEHUB_API_TOKEN`` set with your API token, or pass
    it as a named parameter to the constructor.

    Example:
        .. code-block:: python

            from openams.rag.vectordb.embeddings import HuggingFaceHubEmbeddings
            repo_id = "sentence-transformers/all-mpnet-base-v2"
            hf = HuggingFaceHubEmbeddings(
                repo_id=repo_id,
                task="feature-extraction",
                huggingfacehub_api_token="my-api-key",
            )
    """

    client: Any  #: :meta private:
    repo_id: str = DEFAULT_REPO_ID
    """Model name to use."""
    task: Optional[str] = "feature-extraction"
    """Task to call the model with."""
    model_kwargs: Optional[dict] = None
    """Key word arguments to pass to the model."""

    huggingfacehub_api_token: Optional[str] = None

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    @root_validator()
    def validate_environment(cls, values: Dict) -> Dict:
        """Validate that api key and python package exists in environment."""
        huggingfacehub_api_token = get_from_dict_or_env(
            values, "huggingfacehub_api_token", "HUGGINGFACEHUB_API_TOKEN"
        )
        try:
            from huggingface_hub.inference_api import InferenceApi

            repo_id = values["repo_id"]
            if not repo_id.startswith("sentence-transformers"):
                raise ValueError(
                    "Currently only 'sentence-transformers' embedding models "
                    f"are supported. Got invalid 'repo_id' {repo_id}."
                )
            client = InferenceApi(
                repo_id=repo_id,
                token=huggingfacehub_api_token,
                task=values.get("task"),
            )
            if client.task not in VALID_TASKS:
                raise ValueError(
                    f"Got invalid task {client.task}, "
                    f"currently only {VALID_TASKS} are supported"
                )
            values["client"] = client
        except ImportError:
            raise ValueError(
                "Could not import huggingface_hub python package. "
                "Please install it with `pip install huggingface_hub`."
            )
        return values

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Call out to HuggingFaceHub's embedding endpoint for embedding search docs.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        # replace newlines, which can negatively affect performance.
        texts = [text.replace("\n", " ") for text in texts]
        _model_kwargs = self.model_kwargs or {}
        responses = self.client(inputs=texts, params=_model_kwargs)
        return responses

    def embed_query(self, text: str) -> List[float]:
        """Call out to HuggingFaceHub's embedding endpoint for embedding query text.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        response = self.embed_documents([text])[0]
        return response

class HuggingFaceSetenceTransformersEmbeddings(BaseModel, Embeddings):
    """Wrapper around sentence_transformers embedding models.

    To use, you should have the ``sentence_transformers`` python package installed.

    Example:
        .. code-block:: python

            from openams.rag.vectordb.embeddings import HuggingFaceEmbeddings

            model_name = "sentence-transformers/all-mpnet-base-v2"
            model_kwargs = {'device': 'cpu'}
            encode_kwargs = {'normalize_embeddings': False}
            hf = HuggingFaceEmbeddings(
                model_name=model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )
    """

    client: Any  #: :meta private:
    model_name: str = DEFAULT_MODEL_NAME
    """Model name to use."""
    cache_folder: Optional[str] = None
    """Path to store models. 
    Can be also set by SENTENCE_TRANSFORMERS_HOME environment variable."""
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Key word arguments to pass to the model."""
    encode_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Key word arguments to pass when calling the `encode` method of the model."""

    def __init__(self, **kwargs: Any):
        """Initialize the sentence_transformer."""
        super().__init__(**kwargs)
        try:
            import sentence_transformers

        except ImportError as exc:
            raise ImportError(
                "Could not import sentence_transformers python package. "
                "Please install it with `pip install sentence_transformers`."
            ) from exc

        self.client = sentence_transformers.SentenceTransformer(
            self.model_name, cache_folder=self.cache_folder, **self.model_kwargs
        )

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Compute doc embeddings using a HuggingFace transformer model.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        texts = list(map(lambda x: x.replace("\n", " "), texts))
        embeddings = self.client.encode(texts, **self.encode_kwargs)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """Compute query embeddings using a HuggingFace transformer model.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        text = text.replace("\n", " ")
        embedding = self.client.encode(text, **self.encode_kwargs)
        return embedding.tolist()


class HuggingFaceInstructEmbeddings(BaseModel, Embeddings):
    """Wrapper around sentence_transformers embedding models.

    To use, you should have the ``sentence_transformers``
    and ``InstructorEmbedding`` python packages installed.

    Example:
        .. code-block:: python

            from openams.rag.vectordb.embeddings import HuggingFaceInstructEmbeddings

            model_name = "hkunlp/instructor-large"
            model_kwargs = {'device': 'cpu'}
            encode_kwargs = {'normalize_embeddings': True}
            hf = HuggingFaceInstructEmbeddings(
                model_name=model_name,
                model_kwargs=model_kwargs,
                encode_kwargs=encode_kwargs
            )
    """

    client: Any  #: :meta private:
    model_name: str = DEFAULT_INSTRUCT_MODEL
    """Model name to use."""
    cache_folder: Optional[str] = None
    """Path to store models. 
    Can be also set by SENTENCE_TRANSFORMERS_HOME environment variable."""
    model_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Key word arguments to pass to the model."""
    encode_kwargs: Dict[str, Any] = Field(default_factory=dict)
    """Key word arguments to pass when calling the `encode` method of the model."""
    embed_instruction: str = DEFAULT_EMBED_INSTRUCTION
    """Instruction to use for embedding documents."""
    query_instruction: str = DEFAULT_QUERY_INSTRUCTION
    """Instruction to use for embedding query."""

    def __init__(self, **kwargs: Any):
        """Initialize the sentence_transformer."""
        super().__init__(**kwargs)
        try:
            from InstructorEmbedding import INSTRUCTOR

            self.client = INSTRUCTOR(
                self.model_name, cache_folder=self.cache_folder, **self.model_kwargs
            )
        except ImportError as e:
            raise ValueError("Dependencies for InstructorEmbedding not found.") from e

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Compute doc embeddings using a HuggingFace instruct model.

        Args:
            texts: The list of texts to embed.

        Returns:
            List of embeddings, one for each text.
        """
        instruction_pairs = [[self.embed_instruction, text] for text in texts]
        embeddings = self.client.encode(instruction_pairs, **self.encode_kwargs)
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """Compute query embeddings using a HuggingFace instruct model.

        Args:
            text: The text to embed.

        Returns:
            Embeddings for the text.
        """
        instruction_pair = [self.query_instruction, text]
        embedding = self.client.encode([instruction_pair], **self.encode_kwargs)[0]
        return embedding.tolist()