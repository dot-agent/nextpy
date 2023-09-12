"""Wrappers around embedding modules."""
import logging
from typing import Any

from dotagent.vectorstores.embeddings.aleph_alpha import (
    AlephAlphaAsymmetricSemanticEmbedding,
    AlephAlphaSymmetricSemanticEmbedding,
)
from dotagent.vectorstores.embeddings.bedrock import BedrockEmbeddings
from dotagent.vectorstores.embeddings.cohere import CohereEmbeddings
from dotagent.vectorstores.embeddings.dashscope import DashScopeEmbeddings
from dotagent.vectorstores.embeddings.deepinfra import DeepInfraEmbeddings
from dotagent.vectorstores.embeddings.elasticsearch import ElasticsearchEmbeddings
from dotagent.vectorstores.embeddings.embaas import EmbaasEmbeddings
from dotagent.vectorstores.embeddings.fake import FakeEmbeddings
from dotagent.vectorstores.embeddings.google_palm import GooglePalmEmbeddings
from dotagent.vectorstores.embeddings.huggingface import (
    HuggingFaceSetenceTransformersEmbeddings,
    HuggingFaceInstructEmbeddings,
    HuggingFaceHubEmbeddings,
)
from dotagent.vectorstores.embeddings.jina import JinaEmbeddings
from dotagent.vectorstores.embeddings.llamacpp import LlamaCppEmbeddings
from dotagent.vectorstores.embeddings.minimax import MiniMaxEmbeddings
from dotagent.vectorstores.embeddings.modelscopehub import ModelScopeEmbeddings
from dotagent.vectorstores.embeddings.mosaicml import MosaicMLInstructorEmbeddings
from dotagent.vectorstores.embeddings.openai import OpenAIEmbeddings
from dotagent.vectorstores.embeddings.tensorflowhub import TensorflowHubEmbeddings

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

