"""GraphQL Reader."""

from typing import Dict, List, Optional

from openams.rag.document_loaders.basereader import BaseReader
from openams.schema import DocumentNode
import yaml


class GraphQLReader(BaseReader):
    """GraphQL reader.

    Combines all GraphQL results into the DocumentNode used by LlamaIndex.

    Args:
        uri (str): GraphQL uri.
        headers (Optional[Dict]): Optional http headers.

    """

    def __init__(
        self,
        uri: Optional[str] = None,
        headers: Optional[Dict] = None,
    ) -> None:
        """Initialize with parameters."""

        self.uri = uri
        
        try:
            from gql import Client
            from gql.transport.requests import RequestsHTTPTransport

        except ImportError:
            raise ImportError("`gql` package not found, please run `pip install gql`")
        if uri:
            if uri is None:
                raise ValueError("`uri` must be provided.")
            if headers is None:
                headers = {}
            transport = RequestsHTTPTransport(url=uri, headers=headers)
            self.client = Client(transport=transport, fetch_schema_from_transport=True)

    def load_data(self, query: str, variables: Optional[Dict] = None) -> List[DocumentNode]:
        """Run query with optional variables and turn results into documents

        Args:
            query (str): GraphQL query string.
            variables (Optional[Dict]): optional query parameters.

        Returns:
            List[DocumentNode]: A list of documents.

        """

        metadata = {
            "uri": self.uri,
            "query": query,
            "variables": variables
        }

        try:
            from gql import gql

        except ImportError:
            raise ImportError("`gql` package not found, please run `pip install gql`")
        if variables is None:
            variables = {}

        documents = []

        result = self.client.execute(gql(query), variable_values=variables)

        for key in result:
            entry = result[key]
            if type(entry) == list:
                documents.extend([DocumentNode(text=yaml.dump(v), extra_info=metadata) for v in entry])
            else:
                documents.append(DocumentNode(text=yaml.dump(entry), extra_info=metadata))

        return documents
