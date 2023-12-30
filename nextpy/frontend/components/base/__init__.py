# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Base components."""

from .body import Body
from .document import DocumentHead, Html, Main, NextScript
from .fragment import Fragment
from .head import Head
from .link import RawLink, ScriptTag
from .meta import Description, Image, Meta, Title
from .script import Script

fragment = Fragment.create
script = Script.create
