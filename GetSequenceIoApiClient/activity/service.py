"""Activity and transfers API methods grouped into a service class."""
from __future__ import annotations

from typing import Callable, List, Optional

from .._base import BaseClient, API_BASE_URL
from .._params import (
    CardTransactionsListParams,
    ExternalTransactionsListParams,
    TransfersByAccountListParams,
    TransfersListParams,
)
from .._types import CreateTransferRequest, Headers
from ..models import ExternalTransaction, Transaction, Transfer


class ActivityService:
    def __init__(
        self,
        base: Optional[BaseClient] = None,
        *,
        request_func: Optional[Callable] = None,
        get_all_pages_func: Optional[Callable] = None,
    ) -> None:
        self._base = base
        # allow building URLs without a base by using API_BASE_URL
        self.base_url = base.base_url if base is not None else API_BASE_URL

        # Allow overriding the request and pagination functions for tests
        if request_func is not None:
            self._request_func = request_func
        elif base is not None:
            self._request_func = base._async_request
        else:
            async def _missing_request(*a, **k):
                raise RuntimeError("No request function provided to ActivityService")

            self._request_func = _missing_request

        if get_all_pages_func is not None:
            self._get_all_pages = get_all_pages_func
        elif base is not None:
            self._get_all_pages = base._async_get_all_pages
        else:
            async def _missing_get_all(url, params):
                raise RuntimeError("No get_all_pages function provided to ActivityService")

            self._get_all_pages = _missing_get_all

    async def async_list_transfers(
        self,
        account_ids: Optional[List[str]] = None,
        direction: Optional[str] = None,
        status: Optional[str] = None,
        execution_mode: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        origin: Optional[str] = None,
        rule_execution_id: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[Transfer]:
        params = TransfersListParams(
            account_ids=account_ids,
            direction=direction,
            status=status,
            execution_mode=execution_mode,
            from_date=from_date,
            to_date=to_date,
            origin=origin,
            rule_execution_id=rule_execution_id,
            page=page,
            page_size=page_size,
        ).to_params()

        url = f"{self.base_url}/transfers"
        if page is not None:
            data = await self._request_func("GET", url, params=params)
            items = data.get("items", []) if isinstance(data, dict) else []
        else:
            items = await self._get_all_pages(url, params)

        return [Transfer.from_dict(item) for item in items]

    async def async_list_transfers_by_account(
        self,
        account_id: str,
        account_role: Optional[str] = None,
        direction: Optional[str] = None,
        status: Optional[str] = None,
        execution_mode: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        origin: Optional[str] = None,
        rule_execution_id: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[Transfer]:
        params = TransfersByAccountListParams(
            account_role=account_role,
            direction=direction,
            status=status,
            execution_mode=execution_mode,
            from_date=from_date,
            to_date=to_date,
            origin=origin,
            rule_execution_id=rule_execution_id,
            page=page,
            page_size=page_size,
        ).to_params()

        url = f"{self.base_url}/accounts/{account_id}/transfers"
        if page is not None:
            data = await self._request_func("GET", url, params=params)
            items = data.get("items", []) if isinstance(data, dict) else []
        else:
            items = await self._get_all_pages(url, params)

        return [Transfer.from_dict(item) for item in items]

    async def async_get_transfer(self, transfer_id: str) -> Transfer:
        url = f"{self.base_url}/transfers/{transfer_id}"
        data = await self._request_func("GET", url)
        return Transfer.from_dict(data)

    async def async_create_transfer(
        self,
        source_account_id: str,
        destination_account_id: str,
        amount_in_cents: int,
        description: Optional[str] = None,
        simulation: bool = False,
        idempotency_key: Optional[str] = None,
    ) -> Transfer:
        url = f"{self.base_url}/transfers"
        headers: Headers = {}
        if idempotency_key:
            headers["idempotency-key"] = idempotency_key

        json_data: CreateTransferRequest = {
            "sourceAccountId": source_account_id,
            "destinationAccountId": destination_account_id,
            "amountInCents": amount_in_cents,
            "simulation": simulation,
        }
        if description is not None:
            json_data["description"] = description

        data = await self._request_func("POST", url, headers=headers, json=json_data)
        return Transfer.from_dict(data)

    async def async_list_external_transactions(
        self,
        account_ids: Optional[List[str]] = None,
        direction: Optional[str] = None,
        status: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[ExternalTransaction]:
        params = ExternalTransactionsListParams(
            account_ids=account_ids,
            direction=direction,
            status=status,
            from_date=from_date,
            to_date=to_date,
            page=page,
            page_size=page_size,
        ).to_params()

        url = f"{self.base_url}/external-transactions"
        if page is not None:
            data = await self._request_func("GET", url, params=params)
            items = data.get("items", []) if isinstance(data, dict) else []
        else:
            items = await self._get_all_pages(url, params)

        return [ExternalTransaction.from_dict(item) for item in items]

    async def async_list_card_transactions(
        self,
        account_id: Optional[str] = None,
        card_id: Optional[str] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        page: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> List[Transaction]:
        params = CardTransactionsListParams(
            account_id=account_id,
            card_id=card_id,
            from_date=from_date,
            to_date=to_date,
            page=page,
            page_size=page_size,
        ).to_params()

        url = f"{self.base_url}/card-transactions"
        if page is not None:
            data = await self._request_func("GET", url, params=params)
            items = data.get("items", []) if isinstance(data, dict) else []
        else:
            items = await self._get_all_pages(url, params)

        return [Transaction.from_dict(item) for item in items]
