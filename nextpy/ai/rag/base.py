from typing import List


class SimpleRAG:
    def __init__(self, raw_data=None, data_transformer=None, vector_store=None):
        """Initialize the knowledge base.

        Args:
            raw_data: The raw data to add to the knowledge base. Default is None.
            data_transformer: An object with a `split_documents` method to apply to the raw data. Default is None.
            vector_store: An object with `add_documents` and `similarity_search` methods to use for storing vectors. Default is None.
        """
        self.data_transformer = data_transformer
        self.vector_store = vector_store
        self.references = []
        self.add_data(raw_data)

    def add_data(self, raw_data):
        """Add raw data into the knowledge base.

        Args:
            raw_data: The raw data to add.
        """
        # Validate raw data
        if not raw_data:
            raise ValueError("Raw data cannot be empty.")

        # fetch and add references
        for data in raw_data:
            self.references.append(data.metadata)

        # Split raw data into chunks
        split_data = self.data_transformer.split_documents(raw_data)

        # Add split data to vector store
        try:
            self.vector_store.add_documents(split_data)
        except Exception as e:
            print(f"Failed to add documents: {e}")
            raise

    def retrieve_data(self, query, top_k=1) -> List[str]:
        """Retrieve documents from the knowledge base.

        Args:
            query: The query to use for the retrieval.
            top_k: The number of documents to retrieve. Default is 1.

        Returns:
            A list of the retrieved documents.
        """
        try:
            results = self.vector_store.similarity_search(query=query, top_k=top_k)
        except Exception as e:
            print(f"Failed to retrieve documents: {e}")
            raise

        # Handle no results case
        if not results:
            return []

        # Extract page content
        docs = [result[0].page_content for result in results]
        return docs
