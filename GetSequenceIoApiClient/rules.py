"""Rules-related API methods grouped into a service class."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ._base import BaseClient
from .models import Rule, RuleExecution, RuleExecutionSummary, RuleSummary


class RulesService:
    def __init__(self, base: BaseClient) -> None:
        self._base = base

    async def async_list_rules(
        self,
        source_id: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[RuleSummary]:
        params: Dict[str, Any] = {}
        if source_id:
            params["sourceId"] = source_id
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["pageSize"] = page_size

        url = f"{self._base.base_url}/rules"
        if page is not None:
            data = await self._base._async_request("GET", url, params=params)
            items = data.get("items", []) if isinstance(data, dict) else []
        else:
            items = await self._base._async_get_all_pages(url, params)

        return [RuleSummary.from_dict(item) for item in items]

    async def async_get_rule(self, rule_id: str) -> Rule:
        url = f"{self._base.base_url}/rules/{rule_id}"
        data = await self._base._async_request("GET", url)
        return Rule.from_dict(data)

    async def async_trigger_rule(
        self,
        rule_id: str,
        execute_amount: Optional[int] = None,
        simulation: bool = False,
        idempotency_key: Optional[str] = None,
    ) -> str:
        url = f"{self._base.base_url}/rules/{rule_id}/trigger"
        headers: Dict[str, str] = {}
        if idempotency_key:
            headers["idempotency-key"] = idempotency_key

        json_data: Dict[str, Any] = {"simulation": simulation}
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
        params: Dict[str, Any] = {}
        if status:
            params["status"] = status
        if trigger_type:
            params["triggerType"] = trigger_type
        if execution_mode:
            params["executionMode"] = execution_mode
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["pageSize"] = page_size

        url = f"{self._base.base_url}/rules/{rule_id}/executions"
        if page is not None:
            data = await self._base._async_request("GET", url, params=params)
            items = data.get("items", []) if isinstance(data, dict) else []
        else:
            items = await self._base._async_get_all_pages(url, params)

        return [RuleExecutionSummary.from_dict(item) for item in items]

    async def async_get_rule_execution(self, rule_id: str, execution_id: str) -> RuleExecution:
        url = f"{self._base.base_url}/rules/{rule_id}/executions/{execution_id}"
        data = await self._base._async_request("GET", url)
        return RuleExecution.from_dict(data)
