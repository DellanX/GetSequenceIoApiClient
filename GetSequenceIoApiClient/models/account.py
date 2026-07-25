from __future__ import annotations

from typing import Optional

from pydantic import Field

from .account_summary import AccountSummary
from .balance import Balance
from .linked_account import LinkedAccount


class Account(AccountSummary):
    """Full account representation including masked account details and current balance."""

    routing_number: Optional[str] = Field(default=None, alias="routingNumber")
    bank_account_number: Optional[str] = Field(default=None, alias="bankAccountNumber")
    balance: Optional[Balance] = None
    savings_target_in_cents: Optional[int] = Field(default=None, alias="savingsTargetInCents")
    linked_account: Optional[LinkedAccount] = Field(default=None, alias="linkedAccount")

    @property
    def savings_target_in_dollars(self) -> Optional[float]:
        """Savings goal in dollars."""

        if self.savings_target_in_cents is None:
            return None
        return self.savings_target_in_cents / 100.0
