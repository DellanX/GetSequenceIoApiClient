from __future__ import annotations

from typing import Optional

from pydantic import Field

from ._base import SequenceModel
from .transaction_direction import TransactionDirection
from .transaction_status import TransactionStatus


class ExternalTransaction(SequenceModel):
    """Transaction from Plaid-connected external accounts."""

    id: str = ""
    account_id: str = Field(default="", alias="accountId")
    amount_in_cents: int = Field(default=0, alias="amountInCents")
    direction: Optional[TransactionDirection] = None
    status: Optional[TransactionStatus] = None
    description: str = ""
    transaction_date: str = Field(default="", alias="transactionDate")

    @property
    def amount_in_dollars(self) -> float:
        """Transaction amount in dollars."""

        return self.amount_in_cents / 100.0
