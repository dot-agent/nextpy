from tools.wrappers.youtubeSearch import YouTubeSearchTool
from tools.wrappers.youtubeTranscript import YoutubeTranscriptReader
YoutubeSearch = YouTubeSearchTool()

print(YoutubeSearch.run("Samay Raina", 3))

loader  = YoutubeTranscriptReader()
docs = loader.load_data(ytlinks=['https://www.youtube.com/watch?v=i3OYlaoj-BM'])

print(docs)

#Requires installing
#pip install youtube_search
#pip install youtube_transcript_api