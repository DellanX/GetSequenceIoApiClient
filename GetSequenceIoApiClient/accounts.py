"""Accounts-related API methods grouped into a service class."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from ._base import BaseClient
from .models import Account, AccountSummary


class AccountsService:
    def __init__(self, base: BaseClient) -> None:
        self._base = base

    async def async_get_accounts(
        self,
        type: Optional[str] = None,
        state: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[AccountSummary]:
        params: Dict[str, Any] = {}
        if type:
            params["type"] = type
        if state:
            params["state"] = state
        if page is not None:
            params["page"] = page
        if page_size is not None:
            params["pageSize"] = page_size

        url = f"{self._base.base_url}/accounts"
        if page is not None:
            data = await self._base._async_request("GET", url, params=params)
            items = data.get("items", []) if isinstance(data, dict) else []
        else:
            items = await self._base._async_get_all_pages(url, params)

        return [AccountSummary.from_dict(item) for item in items]

    async def async_get_account(self, account_id: str) -> Account:
        url = f"{self._base.base_url}/accounts/{account_id}"
        data = await self._base._async_request("GET", url)
        return Account.from_dict(data)

    async def async_test_connection(self) -> bool:
        try:
            await self.async_get_accounts(page=1, page_size=1)
        except Exception:
            return False
        else:
            return True
