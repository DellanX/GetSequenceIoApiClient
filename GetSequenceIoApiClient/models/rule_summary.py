from __future__ import annotations

from typing import Optional

from pydantic import Field

from ._base import SequenceModel


class RuleSummary(SequenceModel):
    """Lightweight rule representation returned by list endpoints."""

    id: str = ""
    name: Optional[str] = None
    description: Optional[str] = None
    status: str = ""
    is_supported: bool = Field(default=False, alias="isSupported")
    created_at: str = Field(default="", alias="createdAt")
    updated_at: str = Field(default="", alias="updatedAt")
    deleted_at: Optional[str] = Field(default=None, alias="deletedAt")