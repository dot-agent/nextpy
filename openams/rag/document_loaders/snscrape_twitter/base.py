"""SnscrapeTwitter reader."""
from typing import List

from openams.rag.document_loaders.basereader import BaseReader
from openams.schema import DocumentNode


class SnscrapeTwitterReader(BaseReader):
    """SnscrapeTwitter reader. Reads data from a twitter profile.

    Args:
        username (str): Twitter Username.
        num_tweets (int): Number of tweets to fetch.
    """

    def __init__(self):
        """Initialize SnscrapeTwitter reader."""

    def load_data(self, username: str, num_tweets: int) -> List[DocumentNode]:
        """Load data from a twitter profile.

        Args:
            username (str): Twitter Username.
            num_tweets (int): Number of tweets to fetch.
        Returns:
            List[DocumentNode]: List of documents.
        """
        import snscrape.modules.twitter as sntwitter

        attributes_container = []
        for i, tweet in enumerate(
            sntwitter.TwitterSearchScraper(f"from:{username}").get_items()
        ):
            if i > num_tweets:
                break
            attributes_container.append(tweet.rawContent)
        return [DocumentNode(text=attributes_container, extra_info={"username": username, "num_tweets": num_tweets})]
