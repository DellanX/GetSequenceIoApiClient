from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class Rule:
    """Full representation of a rule."""

    id: str
    name: Optional[str]
    description: Optional[str]
    status: str
    trigger: Optional[Dict[str, Any]]
    steps: List[Dict[str, Any]]
    created_at: str
    updated_at: str
    deleted_at: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Rule:
        """Parse Rule from a dictionary."""

        return cls(
            id=data.get("id", ""),
            name=data.get("name"),
            description=data.get("description"),
            status=data.get("status", ""),
            trigger=data.get("trigger"),
            steps=data.get("steps", []),
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
            "trigger": self.trigger,
            "steps": self.steps,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "deletedAt": self.deleted_at,
        }