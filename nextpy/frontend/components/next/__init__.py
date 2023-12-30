# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Namespace for components provided by next packages."""

from .base import NextComponent
from .image import Image
from .link import NextLink
from .video import Video

image = Image.create
video = Video.create
next_link = NextLink.create
