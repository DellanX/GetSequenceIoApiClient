"""Audit logs API methods grouped into a service class."""
from __future__ import annotations

from typing import List, Optional

from ._base import BaseClient
from ._params import AuditLogsListParams
from ._resource import BaseResource
from .models import AuditLogEntry


class AuditLogsService(BaseResource):
    def __init__(self, base: BaseClient) -> None:
        super().__init__(base)

    async def async_list_audit_logs(
        self,
        api_key_id: Optional[str] = None,
        action: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[AuditLogEntry]:
        params = AuditLogsListParams(
            api_key_id=api_key_id,
            action=action,
            from_date=from_date,
            to_date=to_date,
            page=page,
            page_size=page_size,
        ).to_params()
        return await self._list_items(
            path="audit-logs",
            params=params,
            page=page,
            item_model=AuditLogEntry,
        )
