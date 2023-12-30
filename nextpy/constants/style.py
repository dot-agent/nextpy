# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Style constants."""

import os
from types import SimpleNamespace

from nextpy.constants.base import Dirs

# The directory where styles are located.
STYLES_DIR = os.path.join(Dirs.WEB, "styles")


class Tailwind(SimpleNamespace):
    """Tailwind constants."""

    # The Tailwindcss version
    VERSION = "tailwindcss@3.3.2"
    # The Tailwind config.
    CONFIG = os.path.join(Dirs.WEB, "tailwind.config.js")
    # Default Tailwind content paths
    CONTENT = ["./pages/**/*.{js,ts,jsx,tsx}", "./utils/**/*.{js,ts,jsx,tsx}"]
    # Relative tailwind style path to root stylesheet in STYLES_DIR.
    ROOT_STYLE_PATH = "./tailwind.css"
