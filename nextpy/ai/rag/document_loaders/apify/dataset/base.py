"""Apify dataset reader."""
from typing import Callable, Dict, List

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class ApifyDataset(BaseReader):
    """Apify Dataset reader.
    Reads a dataset on the Apify platform.

    Args:
        apify_api_token (str): Apify API token.
    """

    def __init__(self, apify_api_token: str) -> None:
        """Initialize Apify dataset reader."""
        from apify_client import ApifyClient

        self.apify_client = ApifyClient(apify_api_token)

    def load_data(
        self, dataset_id: str, dataset_mapping_function: Callable[[Dict], DocumentNode]
    ) -> List[DocumentNode]:
        """Load data from the Apify dataset.
        Args:
            dataset_id (str): Dataset ID.
            dataset_mapping_function (Callable[[Dict], DocumentNode]): Function to map dataset items to DocumentNode.

        Returns:
            List[DocumentNode]: List of documents.
        """
        items_list = self.apify_client.dataset(dataset_id).list_items(clean=True)

        document_list = []
        for item in items_list.items:
            DocumentNode = dataset_mapping_function(item)
            if not isinstance(DocumentNode, DocumentNode):
                raise ValueError("Dataset_mapping_function must return a DocumentNode")
            document_list.append(DocumentNode)

        return document_list
