"""Accounts-related API methods grouped into a service class."""
from __future__ import annotations

from typing import List, Optional

from ._base import BaseClient
from ._params import AccountsListParams
from ._resource import BaseResource
from .models import Account, AccountSummary


class AccountsService(BaseResource):
    def __init__(self, base: BaseClient) -> None:
        super().__init__(base)

    async def async_get_accounts(
        self,
        type: Optional[str] = None,
        state: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[AccountSummary]:
        params = AccountsListParams(
            type=type,
            state=state,
            page=page,
            page_size=page_size,
        ).to_params()
        return await self._list_items(
            path="accounts",
            params=params,
            page=page,
            item_model=AccountSummary,
        )

    async def async_get_account(self, account_id: str) -> Account:
        url = self._url(f"accounts/{account_id}")
        data = await self._base._async_request("GET", url)
        return Account.from_dict(data)

    async def async_test_connection(self) -> bool:
        try:
            await self.async_get_accounts(page=1, page_size=1)
        except Exception:
            return False
        else:
            return True
