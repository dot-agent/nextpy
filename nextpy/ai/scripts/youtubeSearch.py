import json

from nextpy.ai.tools.basetool import BaseTool


class YouTubeSearchTool(BaseTool):
    """Tool that queries YouTube."""

    name = "youtube_search"
    description = (
        "search for youtube videos associated with a person. "
        "the input to this tool should be a comma separated list, "
        "the first part contains a person name and the second a "
        "number that is the maximum number of video results "
        "to return aka num_results. the second part is optional"
    )

    def _search(self, person: str, num_results: int) -> str:
        from youtube_search import YoutubeSearch

        results = YoutubeSearch(person, num_results).to_json()
        data = json.loads(results)
        url_suffix_list = [video["url_suffix"] for video in data["videos"]]
        return str(url_suffix_list)

    def run(
        self,
        query: str,
    ) -> str:
        """Use the tool."""
        values = query.split(",")
        person = values[0]
        num_results = int(values[1]) if len(values) > 1 else 2
        return self._search(person, num_results)

    async def _arun(self, query: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("YouTubeSearchTool  does not yet support async")
