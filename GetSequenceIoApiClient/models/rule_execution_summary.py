from __future__ import annotations

from typing import Optional

from pydantic import Field

from ._base import SequenceModel
from .execution_mode import ExecutionMode
from .rule_execution_status import RuleExecutionStatus


class RuleExecutionSummary(SequenceModel):
    """Lightweight rule execution representation."""

    id: str = ""
    rule_id: str = Field(default="", alias="ruleId")
    status: Optional[RuleExecutionStatus] = None
    execution_mode: Optional[ExecutionMode] = Field(default=None, alias="executionMode")
    created_at: str = Field(default="", alias="createdAt")