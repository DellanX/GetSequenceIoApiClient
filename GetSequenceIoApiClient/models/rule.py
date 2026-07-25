from __future__ import annotations

from typing import Optional

from pydantic import Field

from .rule_schema import RuleStep, Trigger
from ._base import SequenceModel


class Rule(SequenceModel):
    """Full representation of a rule."""

    id: str = ""
    name: Optional[str] = None
    description: Optional[str] = None
    status: str = ""
    trigger: Optional[Trigger] = None
    steps: list[RuleStep] = Field(default_factory=list)
    created_at: str = Field(default="", alias="createdAt")
    updated_at: str = Field(default="", alias="updatedAt")
    deleted_at: Optional[str] = Field(default=None, alias="deletedAt")