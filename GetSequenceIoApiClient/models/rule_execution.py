from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .rule_execution_summary import RuleExecutionSummary


@dataclass
class RuleExecution(RuleExecutionSummary):
    """Full rule execution details."""

    trigger_details: Optional[Dict[str, Any]]
    step_index_matched: Optional[int]
    conditions_not_met: bool
    transfers_attempted: int
    transfers_completed: int
    transfers_failed: int
    transfers_pending: int
    transfer_ids: List[str]
    error_message: Optional[str]
    next_attempt_at: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RuleExecution:
        """Parse RuleExecution from a dictionary."""

        summary = RuleExecutionSummary.from_dict(data)
        return cls(
            id=summary.id,
            rule_id=summary.rule_id,
            status=summary.status,
            execution_mode=summary.execution_mode,
            created_at=summary.created_at,
            trigger_details=data.get("triggerDetails") if "triggerDetails" in data else data.get("trigger_details"),
            step_index_matched=data.get("stepIndexMatched") if "stepIndexMatched" in data else data.get("step_index_matched"),
            conditions_not_met=data.get("conditionsNotMet") if "conditionsNotMet" in data else data.get("conditions_not_met", False),
            transfers_attempted=data.get("transfersAttempted") if "transfersAttempted" in data else data.get("transfers_attempted", 0),
            transfers_completed=data.get("transfersCompleted") if "transfersCompleted" in data else data.get("transfers_completed", 0),
            transfers_failed=data.get("transfersFailed") if "transfersFailed" in data else data.get("transfers_failed", 0),
            transfers_pending=data.get("transfersPending") if "transfersPending" in data else data.get("transfers_pending", 0),
            transfer_ids=data.get("transferIds") if "transferIds" in data else data.get("transfer_ids", []),
            error_message=data.get("errorMessage") if "errorMessage" in data else data.get("error_message"),
            next_attempt_at=data.get("nextAttemptAt") if "nextAttemptAt" in data else data.get("next_attempt_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""

        d = super().to_dict()
        d.update(
            {
                "triggerDetails": self.trigger_details,
                "stepIndexMatched": self.step_index_matched,
                "conditionsNotMet": self.conditions_not_met,
                "transfersAttempted": self.transfers_attempted,
                "transfersCompleted": self.transfers_completed,
                "transfersFailed": self.transfers_failed,
                "transfersPending": self.transfers_pending,
                "transferIds": self.transfer_ids,
                "errorMessage": self.error_message,
                "nextAttemptAt": self.next_attempt_at,
            }
        )
        return d