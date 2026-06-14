from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .account_type import AccountType


@dataclass
class LinkedAccountSummary:
    """Lightweight representation of a linked account."""

    id: str
    name: str
    type: AccountType
    description: Optional[str]
    external_account_type: Optional[str]
    beneficiary_name: Optional[str]
    institution_name: Optional[str]
    can_be_source: bool
    can_be_destination: bool
    created_at: str
    updated_at: str
    deleted_at: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> LinkedAccountSummary:
        """Parse LinkedAccountSummary from a dictionary."""

        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            type=AccountType(data["type"]) if isinstance(data.get("type"), str) else data.get("type"),
            description=data.get("description"),
            external_account_type=data.get("externalAccountType") if "externalAccountType" in data else data.get("external_account_type"),
            beneficiary_name=data.get("beneficiaryName") if "beneficiaryName" in data else data.get("beneficiary_name"),
            institution_name=data.get("institutionName") if "institutionName" in data else data.get("institution_name"),
            can_be_source=data.get("canBeSource") if "canBeSource" in data else data.get("can_be_source", False),
            can_be_destination=data.get("canBeDestination") if "canBeDestination" in data else data.get("can_be_destination", False),
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            updated_at=data.get("updatedAt") if "updatedAt" in data else data.get("updated_at", ""),
            deleted_at=data.get("deletedAt") if "deletedAt" in data else data.get("deleted_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary with original camelCase keys."""

        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value if isinstance(self.type, AccountType) else self.type,
            "description": self.description,
            "externalAccountType": self.external_account_type,
            "beneficiaryName": self.beneficiary_name,
            "institutionName": self.institution_name,
            "canBeSource": self.can_be_source,
            "canBeDestination": self.can_be_destination,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "deletedAt": self.deleted_at,
        }