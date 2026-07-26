"""Rules-related API methods grouped into a service class."""
from __future__ import annotations

from typing import List, Optional

from .._base import BaseClient
from .._params import RuleExecutionListParams, RulesListParams
from .._resource import BaseResource
from .._types import Headers, TriggerRuleRequest
from ..models import Rule, RuleExecution, RuleExecutionSummary, RuleSummary


class RulesService(BaseResource):
    def __init__(self, base: BaseClient) -> None:
        super().__init__(base)

    async def async_list_rules(
        self,
        source_id: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[RuleSummary]:
        params = RulesListParams(
            source_id=source_id,
            page=page,
            page_size=page_size,
        ).to_params()
        return await self._list_items(
            path="rules",
            params=params,
            page=page,
            item_model=RuleSummary,
        )

    async def async_get_rule(self, rule_id: str) -> Rule:
        url = self._url(f"rules/{rule_id}")
        data = await self._base._async_request("GET", url)
        return Rule.from_dict(data)

    async def async_trigger_rule(
        self,
        rule_id: str,
        execute_amount: Optional[int] = None,
        simulation: bool = False,
        idempotency_key: Optional[str] = None,
    ) -> str:
        url = self._url(f"rules/{rule_id}/trigger")
        headers: Headers = {}
        if idempotency_key:
            headers["idempotency-key"] = idempotency_key

        json_data: TriggerRuleRequest = {"simulation": simulation}
        if execute_amount is not None:
            json_data["executeAmount"] = execute_amount

        data = await self._base._async_request("POST", url, headers=headers, json=json_data)
        return data.get("executionId", "")

    async def async_list_rule_executions(
        self,
        rule_id: str,
        status: Optional[str] = None,
        trigger_type: Optional[str] = None,
        execution_mode: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[RuleExecutionSummary]:
        params = RuleExecutionListParams(
            status=status,
            trigger_type=trigger_type,
            execution_mode=execution_mode,
            from_date=from_date,
            to_date=to_date,
            page=page,
            page_size=page_size,
        ).to_params()
        return await self._list_items(
            path=f"rules/{rule_id}/executions",
            params=params,
            page=page,
            item_model=RuleExecutionSummary,
        )

    async def async_get_rule_execution(self, rule_id: str, execution_id: str) -> RuleExecution:
        url = self._url(f"rules/{rule_id}/executions/{execution_id}")
        data = await self._base._async_request("GET", url)
        return RuleExecution.from_dict(data)
