from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .balance import Balance
from .linked_account_summary import LinkedAccountSummary


@dataclass
class LinkedAccount(LinkedAccountSummary):
    """Full representation of a linked account."""

    routing_number: Optional[str]
    bank_account_number: Optional[str]
    balance: Optional[Balance]
    savings_target_in_cents: Optional[int]

    @property
    def savings_target_in_dollars(self) -> Optional[float]:
        """Savings goal in dollars."""

        if self.savings_target_in_cents is None:
            return None
        return self.savings_target_in_cents / 100.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> LinkedAccount:
        """Parse LinkedAccount from a dictionary."""

        summary = LinkedAccountSummary.from_dict(data)
        bal_data = data.get("balance")
        balance = Balance.from_dict(bal_data) if isinstance(bal_data, dict) else bal_data
        return cls(
            id=summary.id,
            name=summary.name,
            type=summary.type,
            description=summary.description,
            external_account_type=summary.external_account_type,
            beneficiary_name=summary.beneficiary_name,
            institution_name=summary.institution_name,
            can_be_source=summary.can_be_source,
            can_be_destination=summary.can_be_destination,
            created_at=summary.created_at,
            updated_at=summary.updated_at,
            deleted_at=summary.deleted_at,
            routing_number=data.get("routingNumber") if "routingNumber" in data else data.get("routing_number"),
            bank_account_number=data.get("bankAccountNumber") if "bankAccountNumber" in data else data.get("bank_account_number"),
            balance=balance,
            savings_target_in_cents=data.get("savingsTargetInCents") if "savingsTargetInCents" in data else data.get("savings_target_in_cents"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary with original camelCase keys."""

        d = super().to_dict()
        d.update(
            {
                "routingNumber": self.routing_number,
                "bankAccountNumber": self.bank_account_number,
                "balance": self.balance.to_dict() if self.balance else None,
                "savingsTargetInCents": self.savings_target_in_cents,
            }
        )
        return d