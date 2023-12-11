"""Wrappers around embedding modules."""
import logging
from typing import Any

from nextpy.ai.models.embedding.aleph_alpha import (
    AlephAlphaAsymmetricSemanticEmbedding,
    AlephAlphaSymmetricSemanticEmbedding,
)
from nextpy.ai.models.embedding.bedrock import BedrockEmbeddings
from nextpy.ai.models.embedding.cohere import CohereEmbeddings
from nextpy.ai.models.embedding.dashscope import DashScopeEmbeddings
from nextpy.ai.models.embedding.deepinfra import DeepInfraEmbeddings
from nextpy.ai.models.embedding.elasticsearch import ElasticsearchEmbeddings
from nextpy.ai.models.embedding.embaas import EmbaasEmbeddings
from nextpy.ai.models.embedding.fake import FakeEmbeddings
from nextpy.ai.models.embedding.google_palm import GooglePalmEmbeddings
from nextpy.ai.models.embedding.huggingface import (
    HuggingFaceHubEmbeddings,
    HuggingFaceInstructEmbeddings,
    HuggingFaceSetenceTransformersEmbeddings,
)
from nextpy.ai.models.embedding.jina import JinaEmbeddings
from nextpy.ai.models.embedding.llamacpp import LlamaCppEmbeddings
from nextpy.ai.models.embedding.minimax import MiniMaxEmbeddings
from nextpy.ai.models.embedding.modelscopehub import ModelScopeEmbeddings
from nextpy.ai.models.embedding.mosaicml import MosaicMLInstructorEmbeddings
from nextpy.ai.models.embedding.openai import OpenAIEmbeddings
from nextpy.ai.models.embedding.tensorflowhub import TensorflowHubEmbeddings

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
