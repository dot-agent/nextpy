# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

import os

from nextpy.ai.models.audio.speech_to_text.base import SpeechToText


def get_speech_to_text() -> SpeechToText:
    use = os.getenv("SPEECH_TO_TEXT_USE", "LOCAL_WHISPER")
    if use == "GOOGLE":
        from nextpy.ai.audio.speech_to_text.google import Google

        Google.initialize()
        return Google.get_instance()
    elif use == "LOCAL_WHISPER":
        from nextpy.ai.audio.speech_to_text.whisper import Whisper

        Whisper.initialize(use="local")
        return Whisper.get_instance()
    elif use == "OPENAI_WHISPER":
        from nextpy.ai.audio.speech_to_text.whisper import Whisper

        Whisper.initialize(use="api")
        return Whisper.get_instance()
    else:
        raise NotImplementedError(f"Unknown speech to text engine: {use}")
