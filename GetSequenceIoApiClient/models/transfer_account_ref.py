from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class TransferAccountRef:
    """Reference to an account inside a Transfer."""

    id: Optional[str]
    name: str
    type: str
    is_deleted: Optional[bool]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TransferAccountRef:
        """Parse TransferAccountRef from a dictionary."""

        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            type=data.get("type", ""),
            is_deleted=data.get("isDeleted") if "isDeleted" in data else data.get("is_deleted"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""

        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "isDeleted": self.is_deleted,
        }