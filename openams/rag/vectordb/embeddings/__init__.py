"""Wrappers around embedding modules."""
import logging
from typing import Any

from openams.rag.vectordb.embeddings.aleph_alpha import (
    AlephAlphaAsymmetricSemanticEmbedding,
    AlephAlphaSymmetricSemanticEmbedding,
)
from openams.rag.vectordb.embeddings.bedrock import BedrockEmbeddings
from openams.rag.vectordb.embeddings.cohere import CohereEmbeddings
from openams.rag.vectordb.embeddings.dashscope import DashScopeEmbeddings
from openams.rag.vectordb.embeddings.deepinfra import DeepInfraEmbeddings
from openams.rag.vectordb.embeddings.elasticsearch import ElasticsearchEmbeddings
from openams.rag.vectordb.embeddings.embaas import EmbaasEmbeddings
from openams.rag.vectordb.embeddings.fake import FakeEmbeddings
from openams.rag.vectordb.embeddings.google_palm import GooglePalmEmbeddings
from openams.rag.vectordb.embeddings.huggingface import (
    HuggingFaceSetenceTransformersEmbeddings,
    HuggingFaceInstructEmbeddings,
    HuggingFaceHubEmbeddings,
)
from openams.rag.vectordb.embeddings.jina import JinaEmbeddings
from openams.rag.vectordb.embeddings.llamacpp import LlamaCppEmbeddings
from openams.rag.vectordb.embeddings.minimax import MiniMaxEmbeddings
from openams.rag.vectordb.embeddings.modelscopehub import ModelScopeEmbeddings
from openams.rag.vectordb.embeddings.mosaicml import MosaicMLInstructorEmbeddings
from openams.rag.vectordb.embeddings.openai import OpenAIEmbeddings
from openams.rag.vectordb.embeddings.tensorflowhub import TensorflowHubEmbeddings

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

