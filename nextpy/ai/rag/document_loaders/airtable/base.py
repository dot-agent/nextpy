"""Airtable reader."""
from typing import List

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class AirtableReader(BaseReader):
    """Airtable reader. Reads data from a table in a base.

    Args:
        api_key (str): Airtable API key.
    """

    def __init__(self, api_key: str) -> None:
        """Initialize Airtable reader."""
        self.api_key = api_key

    def load_data(self, base_id: str, table_id: str) -> List[DocumentNode]:
        """Load data from a table in a base.

        Args:
            table_id (str): Table ID.
            base_id (str): Base ID.

        Returns:
            List[DocumentNode]: List of LIDocuments.
        """
        from pyairtable import Table

        metadata = {"base_id": base_id, "table_id": table_id}

        table = Table(self.api_key, base_id, table_id)
        all_records = table.all()
        return [DocumentNode(text=f"{all_records}", extra_info=metadata)]
