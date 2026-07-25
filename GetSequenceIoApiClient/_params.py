from __future__ import annotations

from typing import Optional

from pydantic import Field

from .models._base import QueryParamsModel


class AccountsListParams(QueryParamsModel):
    type: Optional[str] = None
    state: Optional[str] = None
    page: Optional[int] = None
    page_size: Optional[int] = Field(default=None, alias="pageSize")


class RulesListParams(QueryParamsModel):
    source_id: Optional[str] = Field(default=None, alias="sourceId")
    page: Optional[int] = None
    page_size: Optional[int] = Field(default=None, alias="pageSize")


class RuleExecutionListParams(QueryParamsModel):
    status: Optional[str] = None
    trigger_type: Optional[str] = Field(default=None, alias="triggerType")
    execution_mode: Optional[str] = Field(default=None, alias="executionMode")
    from_date: Optional[str] = Field(default=None, alias="from")
    to_date: Optional[str] = Field(default=None, alias="to")
    page: Optional[int] = None
    page_size: Optional[int] = Field(default=None, alias="pageSize")


class AuditLogsListParams(QueryParamsModel):
    api_key_id: Optional[str] = Field(default=None, alias="apiKeyId")
    action: Optional[str] = None
    from_date: Optional[str] = Field(default=None, alias="from")
    to_date: Optional[str] = Field(default=None, alias="to")
    page: Optional[int] = None
    page_size: Optional[int] = Field(default=None, alias="pageSize")


class TransfersListParams(QueryParamsModel):
    account_ids: Optional[list[str]] = Field(default=None, alias="accountIds")
    direction: Optional[str] = None
    status: Optional[str] = None
    execution_mode: Optional[str] = Field(default=None, alias="executionMode")
    from_date: Optional[str] = Field(default=None, alias="from")
    to_date: Optional[str] = Field(default=None, alias="to")
    origin: Optional[str] = None
    rule_execution_id: Optional[str] = Field(default=None, alias="rule_execution_id")
    page: Optional[int] = None
    page_size: Optional[int] = Field(default=None, alias="pageSize")


class TransfersByAccountListParams(QueryParamsModel):
    account_role: Optional[str] = Field(default=None, alias="accountRole")
    direction: Optional[str] = None
    status: Optional[str] = None
    execution_mode: Optional[str] = Field(default=None, alias="executionMode")
    from_date: Optional[str] = Field(default=None, alias="from")
    to_date: Optional[str] = Field(default=None, alias="to")
    origin: Optional[str] = None
    rule_execution_id: Optional[str] = Field(default=None, alias="rule_execution_id")
    page: Optional[int] = None
    page_size: Optional[int] = Field(default=None, alias="pageSize")


class ExternalTransactionsListParams(QueryParamsModel):
    account_ids: Optional[list[str]] = Field(default=None, alias="accountIds")
    direction: Optional[str] = None
    status: Optional[str] = None
    from_date: Optional[str] = Field(default=None, alias="from")
    to_date: Optional[str] = Field(default=None, alias="to")
    page: Optional[int] = None
    page_size: Optional[int] = Field(default=None, alias="pageSize")


class CardTransactionsListParams(QueryParamsModel):
    account_id: Optional[str] = Field(default=None, alias="accountId")
    card_id: Optional[str] = Field(default=None, alias="cardId")
    from_date: Optional[str] = Field(default=None, alias="from")
    to_date: Optional[str] = Field(default=None, alias="to")
    page: Optional[int] = None
    page_size: Optional[int] = Field(default=None, alias="pageSize")
