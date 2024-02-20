# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""dad_jokes reader."""

from typing import List

import requests

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class DadJokesReader(BaseReader):
    """Dad jokes reader.

    Reads a random dad joke.

    """

    def _get_random_dad_joke(self):
        response = requests.get(
            "https://icanhazdadjoke.com/", headers={"Accept": "application/json"}
        )
        response.raise_for_status()
        json_data = response.json()
        return json_data["joke"]

    def load_data(self) -> List[DocumentNode]:
        """Return a random dad joke.

        Args:
            None.

        """
        return [DocumentNode(text=self._get_random_dad_joke())]
