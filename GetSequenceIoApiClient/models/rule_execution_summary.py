from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .execution_mode import ExecutionMode
from .rule_execution_status import RuleExecutionStatus


@dataclass
class RuleExecutionSummary:
    """Lightweight rule execution representation."""

    id: str
    rule_id: str
    status: RuleExecutionStatus
    execution_mode: ExecutionMode
    created_at: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RuleExecutionSummary:
        """Parse RuleExecutionSummary from a dictionary."""

        status_raw = data.get("status")
        mode_raw = data.get("executionMode") if "executionMode" in data else data.get("execution_mode")
        return cls(
            id=data.get("id", ""),
            rule_id=data.get("ruleId") if "ruleId" in data else data.get("rule_id", ""),
            status=RuleExecutionStatus(status_raw) if isinstance(status_raw, str) else status_raw,
            execution_mode=ExecutionMode(mode_raw) if isinstance(mode_raw, str) else mode_raw,
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""

        return {
            "id": self.id,
            "ruleId": self.rule_id,
            "status": self.status.value if isinstance(self.status, RuleExecutionStatus) else self.status,
            "executionMode": self.execution_mode.value if isinstance(self.execution_mode, ExecutionMode) else self.execution_mode,
            "createdAt": self.created_at,
        }