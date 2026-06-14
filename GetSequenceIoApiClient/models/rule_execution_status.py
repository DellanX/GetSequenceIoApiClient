from enum import Enum


class RuleExecutionStatus(str, Enum):
    """Statuses for rule executions."""

    EXECUTED = "EXECUTED"
    PARTIAL = "PARTIAL"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"