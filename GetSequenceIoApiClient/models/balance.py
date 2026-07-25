from __future__ import annotations

from typing import Optional

from pydantic import Field

from .._types import JsonObject
from ._base import SequenceModel


class Balance(SequenceModel):
    """Current balance information for an account."""

    balance_in_cents: Optional[int] = Field(default=None, alias="balanceInCents")
    available_balance_in_cents: Optional[int] = Field(default=None, alias="availableBalanceInCents")
    last_statement_balance_in_cents: Optional[int] = Field(default=None, alias="lastStatementBalanceInCents")
    last_statement_date: Optional[str] = Field(default=None, alias="lastStatementDate")
    next_payment_minimum_in_cents: Optional[int] = Field(default=None, alias="nextPaymentMinimumInCents")
    next_payment_due_date: Optional[str] = Field(default=None, alias="nextPaymentDueDate")
    balance_last_updated_at: Optional[str] = Field(default=None, alias="balanceLastUpdatedAt")
    error: Optional[str] = None
    interest_rate_percentage: Optional[float] = Field(default=None, alias="interestRatePercentage")
    original_loan_amount_in_cents: Optional[int] = Field(default=None, alias="originalLoanAmountInCents")

    @property
    def amount_in_dollars(self) -> Optional[float]:
        """Convert balance_in_cents to dollars for backward compatibility."""

        return self.balance_in_dollars

    @property
    def balance_in_dollars(self) -> Optional[float]:
        """Current balance in dollars."""

        if self.balance_in_cents is None:
            return None
        return self.balance_in_cents / 100.0

    @property
    def available_balance_in_dollars(self) -> Optional[float]:
        """Available balance in dollars."""

        if self.available_balance_in_cents is None:
            return None
        return self.available_balance_in_cents / 100.0

    @property
    def last_statement_balance_in_dollars(self) -> Optional[float]:
        """Last statement balance in dollars."""

        if self.last_statement_balance_in_cents is None:
            return None
        return self.last_statement_balance_in_cents / 100.0

    @property
    def next_payment_minimum_in_dollars(self) -> Optional[float]:
        """Next payment minimum due in dollars."""

        if self.next_payment_minimum_in_cents is None:
            return None
        return self.next_payment_minimum_in_cents / 100.0

    @property
    def original_loan_amount_in_dollars(self) -> Optional[float]:
        """Original loan amount in dollars."""

        if self.original_loan_amount_in_cents is None:
            return None
        return self.original_loan_amount_in_cents / 100.0

    def to_dict(self) -> JsonObject:
        """Convert object back to a dictionary with original camelCase keys."""

        data = super().to_dict()
        data["amountInDollars"] = self.balance_in_dollars
        return data