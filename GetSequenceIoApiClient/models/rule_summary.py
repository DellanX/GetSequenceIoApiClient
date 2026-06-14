from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class RuleSummary:
    """Lightweight rule representation returned by list endpoints."""

    id: str
    name: Optional[str]
    description: Optional[str]
    status: str
    is_supported: bool
    created_at: str
    updated_at: str
    deleted_at: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RuleSummary:
        """Parse RuleSummary from a dictionary."""

        return cls(
            id=data.get("id", ""),
            name=data.get("name"),
            description=data.get("description"),
            status=data.get("status", ""),
            is_supported=data.get("isSupported") if "isSupported" in data else data.get("is_supported", False),
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            updated_at=data.get("updatedAt") if "updatedAt" in data else data.get("updated_at", ""),
            deleted_at=data.get("deletedAt") if "deletedAt" in data else data.get("deleted_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""

        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "isSupported": self.is_supported,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "deletedAt": self.deleted_at,
        }