# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

from abc import ABC, abstractmethod


class SpeechToText(ABC):
    @abstractmethod
    def transcribe(
        self, audio_bytes, platform="web", prompt="", language="en-US"
    ) -> str:
        # platform: 'web' | 'mobile' | 'terminal'
        pass
