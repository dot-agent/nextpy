"""Anonymous telemetry for Nextpy."""

from __future__ import annotations

import json
import multiprocessing
import platform
from datetime import datetime

import psutil

from nextpy import constants


def get_os() -> str:
    """Get the operating system.

    Returns:
        The operating system.
    """
    return platform.system()


def get_python_version() -> str:
    """Get the Python version.

    Returns:
        The Python version.
    """
    return platform.python_version()


def get_nextpy_version() -> str:
    """Get the Nextpy version.

    Returns:
        The Nextpy version.
    """
    return constants.Nextpy.VERSION


def get_cpu_count() -> int:
    """Get the number of CPUs.

    Returns:
        The number of CPUs.
    """
    return multiprocessing.cpu_count()


def get_memory() -> int:
    """Get the total memory in MB.

    Returns:
        The total memory in MB.
    """
    return psutil.virtual_memory().total >> 20


def send(event: str, telemetry_enabled: bool | None = None) -> bool:
    """Send anonymous telemetry for Nextpy.

    Args:
        event: The event name.
        telemetry_enabled: Whether to send the telemetry (If None, get from config).

    Returns:
        Whether the telemetry was sent successfully.
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
        with open(constants.Dirs.NEXTPY_JSON) as f:
            nextpy_json = json.load(f)
            distinct_id = nextpy_json["project_hash"]
        post_hog = {
            "api_key": "phc_iw4MfXVMHRImi7K26DsEZtoKGayuobZp6UNLtQJY6aL",
            "event": event,
            "properties": {
                "distinct_id": distinct_id,
                "user_os": get_os(),
                "nextpy_version": get_nextpy_version(),
                "python_version": get_python_version(),
                "cpu_count": get_cpu_count(),
                "memory": get_memory(),
            },
            "timestamp": datetime.utcnow().isoformat(),
        }
        httpx.post("https://us.posthog.com/capture/", json=post_hog)
        return True
    except Exception:
        return False
