from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class Balance:
    """Current balance information for an account."""

    balance_in_cents: Optional[int]
    available_balance_in_cents: Optional[int]
    last_statement_balance_in_cents: Optional[int]
    last_statement_date: Optional[str]
    next_payment_minimum_in_cents: Optional[int]
    next_payment_due_date: Optional[str]
    balance_last_updated_at: Optional[str]
    error: Optional[str]
    interest_rate_percentage: Optional[float]
    original_loan_amount_in_cents: Optional[int]

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

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Balance:
        """Parse Balance from a dictionary supporting both camelCase and snake_case."""

        return cls(
            balance_in_cents=data.get("balanceInCents") if "balanceInCents" in data else data.get("balance_in_cents"),
            available_balance_in_cents=data.get("availableBalanceInCents") if "availableBalanceInCents" in data else data.get("available_balance_in_cents"),
            last_statement_balance_in_cents=data.get("lastStatementBalanceInCents") if "lastStatementBalanceInCents" in data else data.get("last_statement_balance_in_cents"),
            last_statement_date=data.get("lastStatementDate") if "lastStatementDate" in data else data.get("last_statement_date"),
            next_payment_minimum_in_cents=data.get("nextPaymentMinimumInCents") if "nextPaymentMinimumInCents" in data else data.get("next_payment_minimum_in_cents"),
            next_payment_due_date=data.get("nextPaymentDueDate") if "nextPaymentDueDate" in data else data.get("next_payment_due_date"),
            balance_last_updated_at=data.get("balanceLastUpdatedAt") if "balanceLastUpdatedAt" in data else data.get("balance_last_updated_at"),
            error=data.get("error"),
            interest_rate_percentage=data.get("interestRatePercentage") if "interestRatePercentage" in data else data.get("interest_rate_percentage"),
            original_loan_amount_in_cents=data.get("originalLoanAmountInCents") if "originalLoanAmountInCents" in data else data.get("original_loan_amount_in_cents"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary with original camelCase keys."""

        return {
            "balanceInCents": self.balance_in_cents,
            "availableBalanceInCents": self.available_balance_in_cents,
            "lastStatementBalanceInCents": self.last_statement_balance_in_cents,
            "lastStatementDate": self.last_statement_date,
            "nextPaymentMinimumInCents": self.next_payment_minimum_in_cents,
            "nextPaymentDueDate": self.next_payment_due_date,
            "balanceLastUpdatedAt": self.balance_last_updated_at,
            "error": self.error,
            "interestRatePercentage": self.interest_rate_percentage,
            "originalLoanAmountInCents": self.original_loan_amount_in_cents,
            "amountInDollars": self.balance_in_dollars,
        }