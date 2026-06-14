from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AuditLogEntry:
    """An API key audit log entry."""

    id: str
    created_at: str
    api_key_id: str
    api_key_name: str
    path: str
    action: Optional[str]
    request_id: str
    outcome: str
    error_code: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AuditLogEntry:
        """Parse AuditLogEntry from a dictionary."""

        return cls(
            id=data.get("id", ""),
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            api_key_id=data.get("apiKeyId") if "apiKeyId" in data else data.get("api_key_id", ""),
            api_key_name=data.get("apiKeyName") if "apiKeyName" in data else data.get("api_key_name", ""),
            path=data.get("path", ""),
            action=data.get("action"),
            request_id=data.get("requestId") if "requestId" in data else data.get("request_id", ""),
            outcome=data.get("outcome", ""),
            error_code=data.get("errorCode") if "errorCode" in data else data.get("error_code"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""

        return {
            "id": self.id,
            "createdAt": self.created_at,
            "apiKeyId": self.api_key_id,
            "apiKeyName": self.api_key_name,
            "path": self.path,
            "action": self.action,
            "requestId": self.request_id,
            "outcome": self.outcome,
            "errorCode": self.error_code,
        }