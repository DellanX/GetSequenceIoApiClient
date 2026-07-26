from __future__ import annotations

from typing import Mapping, TypeVar

from pydantic import BaseModel, ConfigDict

from .._types import JsonObject, JsonValue, QueryParams

ModelT = TypeVar("ModelT", bound="SequenceModel")


class SequenceModel(BaseModel):
    """Shared Pydantic model behavior for API schemas."""

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        extra="ignore",
    )

    @classmethod
    def from_dict(cls: type[ModelT], data: Mapping[str, JsonValue]) -> ModelT:
        return cls.model_validate(data)

    def to_dict(self) -> JsonObject:
        return self.model_dump(by_alias=True, mode="json")


class QueryParamsModel(SequenceModel):
    """Shared serialization for request query parameter models."""

    def to_params(self) -> QueryParams:
        return self.model_dump(by_alias=True, exclude_none=True, mode="json")
