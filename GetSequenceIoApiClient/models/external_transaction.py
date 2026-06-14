from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .transaction_direction import TransactionDirection
from .transaction_status import TransactionStatus


@dataclass
class ExternalTransaction:
    """Transaction from Plaid-connected external accounts."""

    id: str
    account_id: str
    amount_in_cents: int
    direction: TransactionDirection
    status: TransactionStatus
    description: str
    transaction_date: str

    @property
    def amount_in_dollars(self) -> float:
        """Transaction amount in dollars."""

        return self.amount_in_cents / 100.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ExternalTransaction:
        """Parse ExternalTransaction from a dictionary."""

        return cls(
            id=data.get("id", ""),
            account_id=data.get("accountId") if "accountId" in data else data.get("account_id", ""),
            amount_in_cents=data.get("amountInCents") if "amountInCents" in data else data.get("amount_in_cents", 0),
            direction=TransactionDirection(data["direction"]) if isinstance(data.get("direction"), str) else data.get("direction"),
            status=TransactionStatus(data["status"]) if isinstance(data.get("status"), str) else data.get("status"),
            description=data.get("description", ""),
            transaction_date=data.get("transactionDate") if "transactionDate" in data else data.get("transaction_date", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""

        return {
            "id": self.id,
            "accountId": self.account_id,
            "amountInCents": self.amount_in_cents,
            "direction": self.direction.value if isinstance(self.direction, TransactionDirection) else self.direction,
            "status": self.status.value if isinstance(self.status, TransactionStatus) else self.status,
            "description": self.description,
            "transactionDate": self.transaction_date,
        }