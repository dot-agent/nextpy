"""Common schema objects."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    TypeVar,
    Union,
)
import uuid
from openams.utils.serializable import Serializable
from pydantic import BaseModel, Extra, Field, root_validator
from enum import auto, Enum
from hashlib import sha256

DEFAULT_TEXT_NODE_TMPL = "{metadata_str}\n\n{content}"
DEFAULT_METADATA_TMPL = "{key}: {value}"

RUN_KEY = "__run"

class BaseMessage(Serializable):
    """Message object."""

    content: str
    additional_kwargs: dict = Field(default_factory=dict)

    @property
    @abstractmethod
    def type(self) -> str:
        """Type of the message, used for serialization."""


class BaseMemory(Serializable, ABC):
    """Base interface for memory in chains."""

    class Config:
        """Configuration for this pydantic object."""

        extra = Extra.forbid
        arbitrary_types_allowed = True

    @property
    @abstractmethod
    def memory_variables(self) -> List[str]:
        """Input keys this memory class will load dynamically."""

    @abstractmethod
    def load_memory_variables(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Return key-value pairs given the text input to the chain.

        If None, return all memories
        """

    @abstractmethod
    def save_context(self, inputs: Dict[str, Any], outputs: Dict[str, str]) -> None:
        """Save the context of this model run to memory."""

    @abstractmethod
    def clear(self) -> None:
        """Clear memory contents."""


class Document(Serializable):
    """Interface for interacting with a document."""

    page_content: str
    metadata: dict = Field(default_factory=dict)

class ObjectType(str, Enum):
    TEXT = auto()
    IMAGE = auto()
    INDEX = auto()
    DOCUMENT = auto()


class MetadataMode(str, Enum):
    ALL = auto()
    EMBED = auto()
    LLM = auto()
    NONE = auto()

    
class NodeRelationship(str, Enum):
    """Node relationships used in `BaseNode` class.

    Attributes:
        SOURCE: The node is the source document.
        PREVIOUS: The node is the previous node in the document.
        NEXT: The node is the next node in the document.
        PARENT: The node is the parent node in the document.
        CHILD: The node is a child node in the document.

    """

    SOURCE = auto()
    PREVIOUS = auto()
    NEXT = auto()
    PARENT = auto()
    CHILD = auto()

    
class RelatedNodeInfo(BaseModel):
    node_id: str
    node_type: Optional[ObjectType] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    hash: Optional[str] = None


RelatedNodeType = Union[RelatedNodeInfo, List[RelatedNodeInfo]]


class BaseNode(BaseModel):
    """Base node Object.

    Generic abstract interface for retrievable nodes

    """

    class Config:
        allow_population_by_field_name = True

    id_: str = Field(
        default_factory=lambda: str(uuid.uuid4()), description="Unique ID of the node."
    )
    embedding: Optional[List[float]] = Field(
        default=None, description="Embedding of the node."
    )

    """"
    metadata fields
    - injected as part of the text shown to LLMs as context
    - injected as part of the text for generating embeddings
    - used by vector DBs for metadata filtering

    """
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="A flat dictionary of metadata fields",
        alias="extra_info",
    )
    excluded_embed_metadata_keys: List[str] = Field(
        default_factory=list,
        description="Metadata keys that are exluded from text for the embed model.",
    )
    excluded_llm_metadata_keys: List[str] = Field(
        default_factory=list,
        description="Metadata keys that are exluded from text for the LLM.",
    )
    relationships: Dict[NodeRelationship, RelatedNodeType] = Field(
        default_factory=dict,
        description="A mapping of relationships to other node information.",
    )
    hash: str = Field(default="", description="Hash of the node content.")

    @classmethod
    @abstractmethod
    def get_type(cls) -> str:
        """Get Object type."""

    @abstractmethod
    def get_content(self, metadata_mode: MetadataMode = MetadataMode.ALL) -> str:
        """Get object content."""

    @abstractmethod
    def get_metadata_str(self, mode: MetadataMode = MetadataMode.ALL) -> str:
        """Metadata string."""

    @abstractmethod
    def set_content(self, value: Any) -> None:
        """Set the content of the node."""

    @property
    def node_id(self) -> str:
        return self.id_

    @property
    def source_node(self) -> Optional[RelatedNodeInfo]:
        """Source object node.

        Extracted from the relationships field.

        """
        if NodeRelationship.SOURCE not in self.relationships:
            return None

        relation = self.relationships[NodeRelationship.SOURCE]
        if isinstance(relation, list):
            raise ValueError("Source object must be a single RelatedNodeInfo object")
        return relation

    @property
    def prev_node(self) -> Optional[RelatedNodeInfo]:
        """Prev node."""
        if NodeRelationship.PREVIOUS not in self.relationships:
            return None

        relation = self.relationships[NodeRelationship.PREVIOUS]
        if not isinstance(relation, RelatedNodeInfo):
            raise ValueError("Previous object must be a single RelatedNodeInfo object")
        return relation

    @property
    def next_node(self) -> Optional[RelatedNodeInfo]:
        """Next node."""
        if NodeRelationship.NEXT not in self.relationships:
            return None

        relation = self.relationships[NodeRelationship.NEXT]
        if not isinstance(relation, RelatedNodeInfo):
            raise ValueError("Next object must be a single RelatedNodeInfo object")
        return relation

    @property
    def parent_node(self) -> Optional[RelatedNodeInfo]:
        """Parent node."""
        if NodeRelationship.PARENT not in self.relationships:
            return None

        relation = self.relationships[NodeRelationship.PARENT]
        if not isinstance(relation, RelatedNodeInfo):
            raise ValueError("Parent object must be a single RelatedNodeInfo object")
        return relation

    @property
    def child_nodes(self) -> Optional[List[RelatedNodeInfo]]:
        """Child nodes."""
        if NodeRelationship.CHILD not in self.relationships:
            return None

        relation = self.relationships[NodeRelationship.PARENT]
        if not isinstance(relation, list):
            raise ValueError("Child objects must be a list of RelatedNodeInfo objects.")
        return relation

    @property
    def ref_doc_id(self) -> Optional[str]:
        """Deprecated: Get ref doc id."""
        source_node = self.source_node
        if source_node is None:
            return None
        return source_node.node_id

    @property
    def extra_info(self) -> Dict[str, Any]:
        """TODO: DEPRECATED: Extra info."""
        return self.metadata

    def get_embedding(self) -> List[float]:
        """Get embedding.

        Errors if embedding is None.

        """
        if self.embedding is None:
            raise ValueError("embedding not set.")
        return self.embedding

    def as_related_node_info(self) -> RelatedNodeInfo:
        """Get node as RelatedNodeInfo."""
        return RelatedNodeInfo(
            node_id=self.node_id, metadata=self.metadata, hash=self.hash
        )


class TextNode(BaseNode):
    text: str = Field(default="", description="Text content of the node.")
    start_char_idx: Optional[int] = Field(
        default=None, description="Start char index of the node."
    )
    end_char_idx: Optional[int] = Field(
        default=None, description="End char index of the node."
    )
    text_template: str = Field(
        default=DEFAULT_TEXT_NODE_TMPL,
        description=(
            "Template for how text is formatted, with {content} and "
            "{metadata_str} placeholders."
        ),
    )
    metadata_template: str = Field(
        default=DEFAULT_METADATA_TMPL,
        description=(
            "Template for how metadata is formatted, with {key} and "
            "{value} placeholders."
        ),
    )
    metadata_seperator: str = Field(
        default="\n",
        description="Seperator between metadata fields when converting to string.",
    )

    @root_validator
    def _check_hash(cls, values: dict) -> dict:
        """Generate a hash to represent the node."""
        text = values.get("text", "")
        metadata = values.get("metadata", {})
        doc_identity = str(text) + str(metadata)
        values["hash"] = str(
            sha256(doc_identity.encode("utf-8", "surrogatepass")).hexdigest()
        )
        return values

    @classmethod
    def get_type(cls) -> str:
        """Get Object type."""
        return ObjectType.TEXT

    def get_content(self, metadata_mode: MetadataMode = MetadataMode.NONE) -> str:
        """Get object content."""
        metadata_str = self.get_metadata_str(mode=metadata_mode).strip()
        return self.text_template.format(
            content=self.text, metadata_str=metadata_str
        ).strip()

    def get_metadata_str(self, mode: MetadataMode = MetadataMode.ALL) -> str:
        """metadata info string."""
        if mode == MetadataMode.NONE:
            return ""

        usable_metadata_keys = set(self.metadata.keys())
        if mode == MetadataMode.LLM:
            for key in self.excluded_llm_metadata_keys:
                if key in usable_metadata_keys:
                    usable_metadata_keys.remove(key)
        elif mode == MetadataMode.EMBED:
            for key in self.excluded_embed_metadata_keys:
                if key in usable_metadata_keys:
                    usable_metadata_keys.remove(key)

        return self.metadata_seperator.join(
            [
                self.metadata_template.format(key=key, value=str(value))
                for key, value in self.metadata.items()
                if key in usable_metadata_keys
            ]
        )

    def set_content(self, value: str) -> None:
        """Set the content of the node."""
        self.text = value

    def get_node_info(self) -> Dict[str, Any]:
        """Get node info."""
        return {"start": self.start_char_idx, "end": self.end_char_idx}

    def get_text(self) -> str:
        return self.get_content(metadata_mode=MetadataMode.NONE)

    @property
    def node_info(self) -> Dict[str, Any]:
        """Deprecated: Get node info."""
        return self.get_node_info()


Node = TextNode


class DocumentNode(TextNode):
    """Generic interface for a data document.

    This document connects to data sources.

    """

    # TODO: A lot of backwards compatibility logic here, clean up
    id_: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Unique ID of the node.",
        alias="doc_id",
    )

    _compat_fields = {"doc_id": "id_", "extra_info": "metadata"}

    @classmethod
    def get_type(cls) -> str:
        """Get Document type."""
        return ObjectType.DOCUMENT

    @property
    def doc_id(self) -> str:
        """Get document ID."""
        return self.id_

    def get_doc_id(self) -> str:
        """TODO: Deprecated: Get document ID."""
        return self.id_

    def __setattr__(self, name: str, value: object) -> None:
        if name in self._compat_fields:
            name = self._compat_fields[name]
        super().__setattr__(name, value)

    def to_langchain_format(self) -> Document:
        """Convert struct to LangChain document format."""
        metadata = self.metadata or {}
        return Document(page_content=self.text, metadata=metadata)

    @classmethod
    def from_langchain_format(cls, doc: Document) -> "Document":
        """Convert struct from LangChain document format."""
        return cls(text=doc.page_content, metadata=doc.metadata)

    @classmethod
    def example(cls) -> "Document":
        document = Document(
            text="SAMPLE_TEXT",
            metadata={"filename": "README.md", "category": "codebase"},
        )
        return document

class BaseRetriever(ABC):
    @abstractmethod
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Get documents relevant for a query.

        Args:
            query: string to find relevant documents for

        Returns:
            List of relevant documents
        """

    @abstractmethod
    async def aget_relevant_documents(self, query: str) -> List[Document]:
        """Get documents relevant for a query.

        Args:
            query: string to find relevant documents for

        Returns:
            List of relevant documents
        """


# For backwards compatibility


Memory = BaseMemory

T = TypeVar("T")


class BaseDocumentTransformer(ABC):
    """Base interface for transforming documents."""

    @abstractmethod
    def transform_documents(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Sequence[Document]:
        """Transform a list of documents."""

    @abstractmethod
    async def atransform_documents(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Sequence[Document]:
        """Asynchronously transform a list of documents."""


class AgentBoxStatus(BaseModel):
    """
    Represents the status of a AgentBox instance.
    """

    status: str

    def __str__(self):
        return self.status

    def __repr__(self):
        return f"Status({self.status})"

    def __eq__(self, other):
        return self.__str__() == other.__str__()


class AgentBoxOutput(BaseModel):
    """
    Represents the code execution output of a AgentBox instance.
    """

    type: str
    content: str

    def __str__(self):
        return self.content

    def __repr__(self):
        return f"{self.type}({self.content})"

    def __eq__(self, other):
        return self.__str__() == other.__str__()


class AgentBoxFile(BaseModel):
    """
    Represents a file returned from a AgentBox instance.
    """

    name: str
    content: Optional[bytes] = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"File({self.name})"
