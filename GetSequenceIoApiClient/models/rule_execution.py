from __future__ import annotations

from typing import Optional

from pydantic import Field

from .rule_schema import TriggerDetails
from .rule_execution_summary import RuleExecutionSummary

class RuleExecution(RuleExecutionSummary):
    """Full rule execution details."""

    trigger_details: Optional[TriggerDetails] = Field(default=None, alias="triggerDetails")
    step_index_matched: Optional[int] = Field(default=None, alias="stepIndexMatched")
    conditions_not_met: bool = Field(default=False, alias="conditionsNotMet")
    transfers_attempted: int = Field(default=0, alias="transfersAttempted")
    transfers_completed: int = Field(default=0, alias="transfersCompleted")
    transfers_failed: int = Field(default=0, alias="transfersFailed")
    transfers_pending: int = Field(default=0, alias="transfersPending")
    transfer_ids: list[str] = Field(default_factory=list, alias="transferIds")
    error_message: Optional[str] = Field(default=None, alias="errorMessage")
    next_attempt_at: Optional[str] = Field(default=None, alias="nextAttemptAt")