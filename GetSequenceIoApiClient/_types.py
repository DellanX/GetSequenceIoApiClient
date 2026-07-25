from __future__ import annotations

from typing import TypedDict

JsonPrimitive = str | int | float | bool | None
JsonValue = JsonPrimitive | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject = dict[str, JsonValue]

QueryValue = str | int | float | bool | list[str] | list[int] | list[float]
QueryParams = dict[str, QueryValue]
Headers = dict[str, str]


class PaginationInfo(TypedDict, total=False):
    page: int
    pageSize: int
    hasNextPage: bool


class PaginatedResponse(TypedDict, total=False):
    items: list[JsonObject]
    pagination: PaginationInfo


class ApiErrorDetails(TypedDict, total=False):
    message: str
    code: str


class ApiErrorResponse(TypedDict, total=False):
    error: ApiErrorDetails


class TriggerRuleRequest(TypedDict, total=False):
    simulation: bool
    executeAmount: int


class CreateTransferRequest(TypedDict, total=False):
    sourceAccountId: str
    destinationAccountId: str
    amountInCents: int
    simulation: bool
    description: str
