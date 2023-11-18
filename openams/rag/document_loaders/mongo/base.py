"""Mongo client."""

from typing import Dict, List, Optional

from openams.rag.document_loaders.basereader import BaseReader
from openams.schema import DocumentNode


class SimpleMongoReader(BaseReader):
    """Simple mongo reader.

    Concatenates each Mongo doc into DocumentNode used by LlamaIndex.

    Args:
        host (str): Mongo host.
        port (int): Mongo port.
        max_docs (int): Maximum number of documents to load.

    """

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[int] = None,
        uri: Optional[str] = None,
        max_docs: int = 1000,
    ) -> None:
        """Initialize with parameters."""
        self.host = host
        self.port = port
        self.uri = uri
        try:
            import pymongo  # noqa: F401
            from pymongo import MongoClient  # noqa: F401
        except ImportError:
            raise ImportError(
                "`pymongo` package not found, please run `pip install pymongo`"
            )
        if uri:
            if uri is None:
                raise ValueError("Either `host` and `port` or `uri` must be provided.")
            self.client: MongoClient = MongoClient(uri)
        else:
            if host is None or port is None:
                raise ValueError("Either `host` and `port` or `uri` must be provided.")
            self.client = MongoClient(host, port)
        self.max_docs = max_docs

    def load_data(
        self, db_name: str, collection_name: str, query_dict: Optional[Dict] = None
    ) -> List[DocumentNode]:
        """Load data from the input directory.

        Args:
            db_name (str): name of the database.
            collection_name (str): name of the collection.
            query_dict (Optional[Dict]): query to filter documents.
                Defaults to None

        Returns:
            List[DocumentNode]: A list of documents.

        """
        metadata = {
            "host": self.host,
            "port": self.port,
            "uri": self.uri,
            "db_name": db_name,
            "collection_name": collection_name,
            "query_dict": query_dict
        }
        documents = []
        db = self.client[db_name]
        if query_dict is None:
            cursor = db[collection_name].find()
        else:
            cursor = db[collection_name].find(query_dict)

        for item in cursor:
            if "text" not in item:
                raise ValueError("`text` field not found in Mongo DocumentNode.")
            documents.append(DocumentNode(text=item["text"], extra_info=metadata))
        return documents
