from __future__ import annotations

from typing import Optional

from pydantic import Field

from ._base import SequenceModel
from .account_type import AccountType


class LinkedAccountSummary(SequenceModel):
    """Lightweight representation of a linked account."""

    id: str = ""
    name: str = ""
    type: Optional[AccountType] = None
    description: Optional[str] = None
    external_account_type: Optional[str] = Field(default=None, alias="externalAccountType")
    beneficiary_name: Optional[str] = Field(default=None, alias="beneficiaryName")
    institution_name: Optional[str] = Field(default=None, alias="institutionName")
    can_be_source: bool = Field(default=False, alias="canBeSource")
    can_be_destination: bool = Field(default=False, alias="canBeDestination")
    created_at: str = Field(default="", alias="createdAt")
    updated_at: str = Field(default="", alias="updatedAt")
    deleted_at: Optional[str] = Field(default=None, alias="deletedAt")