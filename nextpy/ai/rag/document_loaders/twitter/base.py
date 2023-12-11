"""Simple reader that reads tweets of a twitter handle."""
from typing import Any, List, Optional

from nextpy.ai.rag.document_loaders.basereader import BaseReader
from nextpy.ai.schema import DocumentNode


class TwitterTweetReader(BaseReader):
    """Twitter tweets reader.

    Read tweets of user twitter handle.

    Check 'https://developer.twitter.com/en/docs/twitter-api/\
        getting-started/getting-access-to-the-twitter-api' \
        on how to get access to twitter API.

    Args:
        bearer_token (str): bearer_token that you get from twitter API.
        num_tweets (Optional[int]): Number of tweets for each user twitter handle.\
            Default is 100 tweets.
    """

    def __init__(
        self,
        bearer_token: str,
        num_tweets: Optional[int] = 100,
    ) -> None:
        """Initialize with parameters."""
        super().__init__()
        self.bearer_token = bearer_token
        self.num_tweets = num_tweets

    def load_data(
        self, twitterhandles: List[str], **load_kwargs: Any
    ) -> List[DocumentNode]:
        """Load tweets of twitter handles.

        Args:
            twitterhandles (List[str]): List of user twitter handles to read tweets.

        """
        import tweepy

        client = tweepy.Client(bearer_token=self.bearer_token)
        results = []
        for username in twitterhandles:
            # tweets = api.user_timeline(screen_name=user, count=self.num_tweets)
            user = client.get_user(username=username)
            tweets = client.get_users_tweets(user.data.id, max_results=self.num_tweets)
            response = " "
            for tweet in tweets.data:
                response = response + tweet.text + "\n"
            metadata = {"username": username}
            results.append(DocumentNode(text=response, extra_info=metadata))
        return results
