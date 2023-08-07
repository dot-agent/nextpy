from importlib import metadata

try:
    # __version__ = metadata.version(__package__)
    __version__ = "0.3.1"
except metadata.PackageNotFoundError:
    # Case where package metadata is not available.
    __version__ = ""
