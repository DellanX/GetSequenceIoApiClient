from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class SequenceClientConfig(BaseModel):
    """Runtime settings for the modular REST client."""

    model_config = ConfigDict(extra="forbid")

    base_url: str = "https://api.getsequence.io/platform/v1"
    timeout_seconds: int = Field(default=30, gt=0)
