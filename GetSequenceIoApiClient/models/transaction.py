from __future__ import annotations

from typing import Optional

from pydantic import Field

from ._base import SequenceModel
from .transaction_direction import TransactionDirection
from .transfer_account_ref import TransferAccountRef


class Transaction(SequenceModel):
    """A settled card transaction on a Sequence-issued card."""

    id: str = ""
    card_id: str = Field(default="", alias="cardId")
    card_type: str = Field(default="", alias="cardType")
    account: Optional[TransferAccountRef] = None
    direction: Optional[TransactionDirection] = None
    subtype: str = ""
    status: str = ""
    amount_in_cents: int = Field(default=0, alias="amountInCents")
    description: str = ""
    created_at: str = Field(default="", alias="createdAt")
    completed_at: str = Field(default="", alias="completedAt")

    @property
    def amount_in_dollars(self) -> float:
        """Transaction amount in dollars."""

        return self.amount_in_cents / 100.0
