import re
from typing import Any, List, Optional

from nextpy.ai.schema import Document, DocumentNode


class YoutubeTranscriptReader:
    """Youtube Transcript reader."""

    @staticmethod
    def _extract_video_id(yt_link) -> Optional[str]:
        # regular expressions to match the different syntax of YouTube links
        patterns = [
            r"^https?://(?:www\.)?youtube\.com/watch\?v=([\w-]+)",
            r"^https?://(?:www\.)?youtube\.com/embed/([\w-]+)",
            r"^https?://youtu\.be/([\w-]+)",
        ]  # youtu.be does not use www

        for pattern in patterns:
            match = re.search(pattern, yt_link)
            if match:
                return match.group(1)

        # return None if no match is found
        return None

    def load_data(
        self,
        ytlinks: List[str],
        languages: Optional[List[str]] = ["en"],
        **load_kwargs: Any
    ) -> List[DocumentNode]:
        """Load data from the input directory.

        Args:
            pages (List[str]): List of youtube links \
                for which transcripts are to be read.

        """
        from youtube_transcript_api import YouTubeTranscriptApi

        results = []
        for link in ytlinks:
            video_id = self._extract_video_id(link)
            srt = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            transcript = ""
            for chunk in srt:
                transcript = transcript + chunk["text"] + "\n"
            results.append(
                DocumentNode(text=transcript, extra_info={"video_id": video_id})
            )
        return results

    def load_langchain_documents(self, **load_kwargs: Any) -> List[Document]:
        """Load data in LangChain document format."""
        docs = self.load_data(**load_kwargs)
        return [d.to_langchain_format() for d in docs]
