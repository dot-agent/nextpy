"""Anonymous telemetry for Nextpy."""

from __future__ import annotations

import json
import multiprocessing
import platform
from datetime import datetime

import psutil

from nextpy import constants
from nextpy.base import Base


def get_os() -> str:
    """Get the operating system.

    Returns:
        str: The name of the operating system the script is running on.
    """
    return platform.system()


def get_python_version() -> str:
    """Get the Python version.

    Returns:
        str: The version of Python currently being used.
    """
    return platform.python_version()


def get_nextpy_version() -> str:
    """Get the Nextpy version.

    Returns:
        str: The version of Nextpy currently in use.
    """
    return constants.Nextpy.VERSION


def get_cpu_count() -> int:
    """Get the number of CPUs.

    Returns:
        int: The number of CPU cores available in the system.
    """
    return multiprocessing.cpu_count()


def get_memory() -> int:
    """Get the total memory in MB.

    Returns:
        int: The total amount of system memory in Megabytes.
    """
    return psutil.virtual_memory().total >> 20


class Telemetry(Base):
    """Class representing anonymous telemetry data for Nextpy.

    Attributes:
        user_os (str): Operating system of the user.
        cpu_count (int): Number of CPUs in the user's system.
        memory (int): Total memory in MB in the user's system.
        nextpy_version (str): Version of Nextpy being used.
        python_version (str): Python version in use.

    """

    def __init__(self):
        """Initialize the Telemetry object with system and Nextpy information."""
        self.user_os = get_os()
        self.cpu_count = get_cpu_count()
        self.memory = get_memory()
        self.nextpy_version = get_nextpy_version()
        self.python_version = get_python_version()


def send(event: str, telemetry_enabled: bool | None = None) -> bool:
    """Send anonymous telemetry data for Nextpy.

    Args:
        event (str): The event name to be logged.
        telemetry_enabled (bool | None, optional): Flag to enable/disable telemetry.
            If None, the configuration is read from the Nextpy config. Defaults to None.

    Returns:
        bool: True if telemetry data is sent successfully, False otherwise.
    """
    import httpx

    from nextpy.build.config import get_config

    # Get the telemetry_enabled from the config if it is not specified.
    if telemetry_enabled is None:
        telemetry_enabled = get_config().telemetry_enabled

    # Return if telemetry is disabled.
    if not telemetry_enabled:
        return False

    try:
        telemetry = Telemetry()
        with open(constants.Dirs.NEXTPY_JSON) as f:
            nextpy_json = json.load(f)
            distinct_id = nextpy_json["project_hash"]
        post_hog = {
            "api_key": "phx_58p5CHyldekrAItCF75hBP45VXHWzstNyWOZfIhCE2Y",
            "event": event,
            "properties": {
                "distinct_id": distinct_id,
                "user_os": telemetry.user_os,
                "nextpy_version": telemetry.nextpy_version,
                "python_version": telemetry.python_version,
                "cpu_count": telemetry.cpu_count,
                "memory": telemetry.memory,
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
        httpx.post("https://app.posthog.com/capture/", json=post_hog)
        return True
    except Exception:
        return False
