from __future__ import annotations

from typing import Optional

from pydantic import Field

from .execution_mode import ExecutionMode
from ._base import SequenceModel
from .transaction_direction import TransactionDirection
from .transfer_account_ref import TransferAccountRef


class Transfer(SequenceModel):
    """A money movement transfer."""

    id: str = ""
    amount_in_cents: int = Field(default=0, alias="amountInCents")
    direction: Optional[TransactionDirection] = None
    origin: str = ""
    source: Optional[TransferAccountRef] = None
    destination: Optional[TransferAccountRef] = None
    status: str = ""
    execution_mode: Optional[ExecutionMode] = Field(default=None, alias="executionMode")
    rule_id: Optional[str] = Field(default=None, alias="ruleId")
    rule_execution_id: Optional[str] = Field(default=None, alias="ruleExecutionId")
    error_code: Optional[str] = Field(default=None, alias="errorCode")
    created_at: str = Field(default="", alias="createdAt")
    completed_at: Optional[str] = Field(default=None, alias="completedAt")

    @property
    def amount_in_dollars(self) -> float:
        """Transfer amount in dollars."""

        return self.amount_in_cents / 100.0
