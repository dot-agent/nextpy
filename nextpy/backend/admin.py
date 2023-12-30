# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""The Nextpy Admin Dashboard."""
from dataclasses import dataclass, field
from typing import Optional

from starlette_admin.base import BaseAdmin as Admin


@dataclass
class AdminDash:
    """Data used to build the admin dashboard."""

    models: list = field(default_factory=list)
    view_overrides: dict = field(default_factory=dict)
    admin: Optional[Admin] = None
