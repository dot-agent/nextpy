"""Wrappers around embedding modules."""
import logging
from typing import Any

from openagent.rag.vectordb.embeddings.aleph_alpha import (
    AlephAlphaAsymmetricSemanticEmbedding,
    AlephAlphaSymmetricSemanticEmbedding,
)
from openagent.rag.vectordb.embeddings.bedrock import BedrockEmbeddings
from openagent.rag.vectordb.embeddings.cohere import CohereEmbeddings
from openagent.rag.vectordb.embeddings.dashscope import DashScopeEmbeddings
from openagent.rag.vectordb.embeddings.deepinfra import DeepInfraEmbeddings
from openagent.rag.vectordb.embeddings.elasticsearch import ElasticsearchEmbeddings
from openagent.rag.vectordb.embeddings.embaas import EmbaasEmbeddings
from openagent.rag.vectordb.embeddings.fake import FakeEmbeddings
from openagent.rag.vectordb.embeddings.google_palm import GooglePalmEmbeddings
from openagent.rag.vectordb.embeddings.huggingface import (
    HuggingFaceSetenceTransformersEmbeddings,
    HuggingFaceInstructEmbeddings,
    HuggingFaceHubEmbeddings,
)
from openagent.rag.vectordb.embeddings.jina import JinaEmbeddings
from openagent.rag.vectordb.embeddings.llamacpp import LlamaCppEmbeddings
from openagent.rag.vectordb.embeddings.minimax import MiniMaxEmbeddings
from openagent.rag.vectordb.embeddings.modelscopehub import ModelScopeEmbeddings
from openagent.rag.vectordb.embeddings.mosaicml import MosaicMLInstructorEmbeddings
from openagent.rag.vectordb.embeddings.openai import OpenAIEmbeddings
from openagent.rag.vectordb.embeddings.tensorflowhub import TensorflowHubEmbeddings

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

