"""Graph Database Cypher Reader."""

from typing import Dict, List, Optional

import yaml

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class GraphDBCypherReader(BaseReader):
    """Graph database Cypher reader.

    Combines all Cypher query results into the DocumentNode type used by LlamaIndex.

    Args:
        uri (str): Graph Database URI
        username (str): Username
        password (str): Password

    """

    def __init__(self, uri: str, username: str, password: str, database: str) -> None:
        """Initialize with parameters."""
        try:
            from neo4j import GraphDatabase, basic_auth

        except ImportError:
            raise ImportError(
                "`neo4j` package not found, please run `pip install neo4j`"
            )
        if uri:
            if uri is None:
                raise ValueError("`uri` must be provided.")
            self.client = GraphDatabase.driver(
                uri=uri, auth=basic_auth(username, password)
            )
            self.database = database

    def load_data(
        self, query: str, parameters: Optional[Dict] = None
    ) -> List[DocumentNode]:
        """Run the Cypher with optional parameters and turn results into documents.

        Args:
            query (str): Graph Cypher query string.
            parameters (Optional[Dict]): optional query parameters.

        Returns:
            List[DocumentNode]: A list of documents.

        """
        metadata = {"query": query, "parameters": parameters}

        if parameters is None:
            parameters = {}

        records, summary, keys = self.client.execute_query(
            query, parameters, database_=self.database
        )

        documents = [
            DocumentNode(text=yaml.dump(entry.data()), extra_info=metadata)
            for entry in records
        ]

        return documents
