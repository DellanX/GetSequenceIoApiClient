from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from .execution_mode import ExecutionMode
from .transaction_direction import TransactionDirection
from .transfer_account_ref import TransferAccountRef


@dataclass
class Transfer:
    """A money movement transfer."""

    id: str
    amount_in_cents: int
    direction: TransactionDirection
    origin: str
    source: Optional[TransferAccountRef]
    destination: Optional[TransferAccountRef]
    status: str
    execution_mode: Optional[ExecutionMode]
    rule_id: Optional[str]
    rule_execution_id: Optional[str]
    error_code: Optional[str]
    created_at: str
    completed_at: Optional[str]

    @property
    def amount_in_dollars(self) -> float:
        """Transfer amount in dollars."""

        return self.amount_in_cents / 100.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Transfer:
        """Parse Transfer from a dictionary."""

        src_data = data.get("source")
        source = TransferAccountRef.from_dict(src_data) if isinstance(src_data, dict) else src_data

        dest_data = data.get("destination")
        destination = TransferAccountRef.from_dict(dest_data) if isinstance(dest_data, dict) else dest_data

        exec_mode = data.get("executionMode") if "executionMode" in data else data.get("execution_mode")

        return cls(
            id=data.get("id", ""),
            amount_in_cents=data.get("amountInCents") if "amountInCents" in data else data.get("amount_in_cents", 0),
            direction=TransactionDirection(data["direction"]) if isinstance(data.get("direction"), str) else data.get("direction"),
            origin=data.get("origin", ""),
            source=source,
            destination=destination,
            status=data.get("status", ""),
            execution_mode=ExecutionMode(exec_mode) if isinstance(exec_mode, str) else exec_mode,
            rule_id=data.get("ruleId") if "ruleId" in data else data.get("rule_id"),
            rule_execution_id=data.get("ruleExecutionId") if "ruleExecutionId" in data else data.get("rule_execution_id"),
            error_code=data.get("errorCode") if "errorCode" in data else data.get("error_code"),
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            completed_at=data.get("completedAt") if "completedAt" in data else data.get("completed_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""

        return {
            "id": self.id,
            "amountInCents": self.amount_in_cents,
            "direction": self.direction.value if isinstance(self.direction, TransactionDirection) else self.direction,
            "origin": self.origin,
            "source": self.source.to_dict() if self.source else None,
            "destination": self.destination.to_dict() if self.destination else None,
            "status": self.status,
            "executionMode": self.execution_mode.value if isinstance(self.execution_mode, ExecutionMode) else self.execution_mode,
            "ruleId": self.rule_id,
            "ruleExecutionId": self.rule_execution_id,
            "errorCode": self.error_code,
            "createdAt": self.created_at,
            "completedAt": self.completed_at,
        }