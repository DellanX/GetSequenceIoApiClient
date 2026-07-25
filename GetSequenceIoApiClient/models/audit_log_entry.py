from __future__ import annotations

from typing import Optional

from pydantic import Field

from ._base import SequenceModel


class AuditLogEntry(SequenceModel):
    """An API key audit log entry."""

    id: str = ""
    created_at: str = Field(default="", alias="createdAt")
    api_key_id: str = Field(default="", alias="apiKeyId")
    api_key_name: str = Field(default="", alias="apiKeyName")
    path: str = ""
    action: Optional[str] = None
    request_id: str = Field(default="", alias="requestId")
    outcome: str = ""
    error_code: Optional[str] = Field(default=None, alias="errorCode")