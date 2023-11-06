from importlib import metadata
from typing import Optional
from . import agent
from . import audio
from . import caches
from . import compiler
from . import helpers
from . import image_gen
from . import knowledgebase
from . import llms
from . import load
from . import memory
from . import tools
from . import utils
from . import vectorstores

try:
    __version__ = metadata.version(__package__)
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""

# Clear up the namespace
del metadata

# Debug options
verbose: bool = False
debug: bool = False