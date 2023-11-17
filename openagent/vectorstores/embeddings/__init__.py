"""Wrappers around embedding modules."""
import logging
from typing import Any

from openagent.vectorstores.embeddings.aleph_alpha import (
    AlephAlphaAsymmetricSemanticEmbedding,
    AlephAlphaSymmetricSemanticEmbedding,
)
from openagent.vectorstores.embeddings.bedrock import BedrockEmbeddings
from openagent.vectorstores.embeddings.cohere import CohereEmbeddings
from openagent.vectorstores.embeddings.dashscope import DashScopeEmbeddings
from openagent.vectorstores.embeddings.deepinfra import DeepInfraEmbeddings
from openagent.vectorstores.embeddings.elasticsearch import ElasticsearchEmbeddings
from openagent.vectorstores.embeddings.embaas import EmbaasEmbeddings
from openagent.vectorstores.embeddings.fake import FakeEmbeddings
from openagent.vectorstores.embeddings.google_palm import GooglePalmEmbeddings
from openagent.vectorstores.embeddings.huggingface import (
    HuggingFaceSetenceTransformersEmbeddings,
    HuggingFaceInstructEmbeddings,
    HuggingFaceHubEmbeddings,
)
from openagent.vectorstores.embeddings.jina import JinaEmbeddings
from openagent.vectorstores.embeddings.llamacpp import LlamaCppEmbeddings
from openagent.vectorstores.embeddings.minimax import MiniMaxEmbeddings
from openagent.vectorstores.embeddings.modelscopehub import ModelScopeEmbeddings
from openagent.vectorstores.embeddings.mosaicml import MosaicMLInstructorEmbeddings
from openagent.vectorstores.embeddings.openai import OpenAIEmbeddings
from openagent.vectorstores.embeddings.tensorflowhub import TensorflowHubEmbeddings

logger = logging.getLogger(__name__)

__all__ = [
    "AlephAlphaAsymmetricSemanticEmbedding",
    "AlephAlphaSymmetricSemanticEmbedding",
    "BedrockEmbeddings",
    "CohereEmbeddings",
    "DashScopeEmbeddings",
    "DeepInfraEmbeddings",
    "ElasticsearchEmbeddings",
    "EmbaasEmbeddings",
    "FakeEmbeddings",
    "GooglePalmEmbeddings",
    "HuggingFaceSetenceTransformersEmbeddings",
    "HuggingFaceInstructEmbeddings",
    "HuggingFaceHubEmbeddings",
    "JinaEmbeddings",
    "LlamaCppEmbeddings",
    "MiniMaxEmbeddings",
    "ModelScopeEmbeddings",
    "MosaicMLInstructorEmbeddings",
    "OpenAIEmbeddings",
    "TensorflowHubEmbeddings",
]

