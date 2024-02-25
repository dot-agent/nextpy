"""Contains proxy components."""

from .animation import animation
from .unstyled import *  # Make sure this line is correctly importing headless

__all__ = ["animation", "headless"]