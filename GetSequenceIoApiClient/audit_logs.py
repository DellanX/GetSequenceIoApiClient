"""Audit logs API methods grouped into a service class."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ._base import BaseClient
from .models import AuditLogEntry


class AuditLogsService:
    def __init__(self, base: BaseClient) -> None:
        self._base = base

    async def async_list_audit_logs(
        self,
        api_key_id: Optional[str] = None,
        action: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[AuditLogEntry]:
        params: Dict[str, Any] = {}
        if api_key_id:
            params["apiKeyId"] = api_key_id
        if action:
            params["action"] = action
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["pageSize"] = page_size

        url = f"{self._base.base_url}/audit-logs"
        if page is not None:
            data = await self._base._async_request("GET", url, params=params)
            items = data.get("items", []) if isinstance(data, dict) else []
        else:
            items = await self._base._async_get_all_pages(url, params)

        return [AuditLogEntry.from_dict(item) for item in items]
