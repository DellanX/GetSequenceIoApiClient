from __future__ import annotations

from typing import Optional

from pydantic import Field

from ._base import SequenceModel


class TransferAccountRef(SequenceModel):
    """Reference to an account inside a Transfer."""

    id: Optional[str] = None
    name: str = ""
    type: str = ""
    is_deleted: Optional[bool] = Field(default=None, alias="isDeleted")