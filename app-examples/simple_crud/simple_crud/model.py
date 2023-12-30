# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

"""Models used by the app."""
from datetime import datetime, timezone

from sqlmodel import Column, DateTime, Field, func

import nextpy as xt


class Product(xt.Model, table=True):
    """Product model."""

    code: str = Field(unique=True)
    created: datetime = Field(
        default=datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )
    updated: datetime = Field(
        default=datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )
    label: str
    image: str
    quantity: int
    category: str
    seller: str
    sender: str

    def dict(self, *args, **kwargs) -> dict:
        """Serialize method."""
        d = super().dict(*args, **kwargs)
        d["created"] = self.created.replace(microsecond=0).isoformat()
        d["updated"] = self.updated.replace(microsecond=0).isoformat()
        return d
