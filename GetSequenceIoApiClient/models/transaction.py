from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .transaction_direction import TransactionDirection
from .transfer_account_ref import TransferAccountRef


@dataclass
class Transaction:
    """A settled card transaction on a Sequence-issued card."""

    id: str
    card_id: str
    card_type: str
    account: TransferAccountRef
    direction: TransactionDirection
    subtype: str
    status: str
    amount_in_cents: int
    description: str
    created_at: str
    completed_at: str

    @property
    def amount_in_dollars(self) -> float:
        """Transaction amount in dollars."""

        return self.amount_in_cents / 100.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Transaction:
        """Parse Transaction from a dictionary."""

        acc_data = data.get("account")
        account = TransferAccountRef.from_dict(acc_data) if isinstance(acc_data, dict) else acc_data
        return cls(
            id=data.get("id", ""),
            card_id=data.get("cardId") if "cardId" in data else data.get("card_id", ""),
            card_type=data.get("cardType") if "cardType" in data else data.get("card_type", ""),
            account=account,
            direction=TransactionDirection(data["direction"]) if isinstance(data.get("direction"), str) else data.get("direction"),
            subtype=data.get("subtype", ""),
            status=data.get("status", ""),
            amount_in_cents=data.get("amountInCents") if "amountInCents" in data else data.get("amount_in_cents", 0),
            description=data.get("description", ""),
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            completed_at=data.get("completedAt") if "completedAt" in data else data.get("completed_at", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""

        return {
            "id": self.id,
            "cardId": self.card_id,
            "cardType": self.card_type,
            "account": self.account.to_dict() if self.account else None,
            "direction": self.direction.value if isinstance(self.direction, TransactionDirection) else self.direction,
            "subtype": self.subtype,
            "status": self.status,
            "amountInCents": self.amount_in_cents,
            "description": self.description,
            "createdAt": self.created_at,
            "completedAt": self.completed_at,
        }