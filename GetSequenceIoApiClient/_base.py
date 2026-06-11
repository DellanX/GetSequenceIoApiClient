"""Shared base client utilities (HTTP request and pagination)."""
from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional, Callable, AsyncContextManager

import aiohttp
import inspect

from .exceptions import (
    SequenceApiError,
    SequenceAuthError,
    SequenceConnectionError,
)

API_BASE_URL = "https://api.getsequence.io/platform/v1"
API_TIMEOUT = 30

_LOGGER = logging.getLogger(__name__)


class BaseClient:
    """Encapsulates HTTP request logic and pagination helpers."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        access_token: str,
        *,
        request_factory: Optional[Callable[..., AsyncContextManager]] = None,
        timeout_ctx_factory: Optional[Callable[[int], AsyncContextManager]] = None,
    ) -> None:
        self.session = session
        self.access_token = access_token
        self.base_url = API_BASE_URL
        # make timeout injectable for tests
        self.timeout = API_TIMEOUT

        # request_factory should return an async-context-manager or awaitable
        # that yields a response when awaited. Default uses the session.
        self._request_factory = (
            request_factory
            if request_factory is not None
            else lambda method, url, headers=None, params=None, json=None: self.session.request(
                method, url, headers=headers, params=params, json=json
            )
        )

        # timeout_ctx_factory should return an async context manager for the
        # provided timeout. Default uses asyncio.timeout.
        self._timeout_ctx_factory = (
            timeout_ctx_factory
            if timeout_ctx_factory is not None
            else (lambda t: asyncio.timeout(t))
        )

    async def _make_request(
        self,
        method: str,
        url: str,
        headers: Dict[str, str],
        params: Optional[Dict[str, Any]],
        json: Optional[Dict[str, Any]],
    ):
        """Return an async-context-manager for the request. Overridable
        for tests via `request_factory` passed to the constructor.
        """
        result = self._request_factory(method, url, headers=headers, params=params, json=json)
        if inspect.isawaitable(result):
            return await result
        return result

    async def _async_request(
        self,
        method: str,
        url: str,
        headers: Optional[Dict[str, str]] = None,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Any:
        req_headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
        if headers:
            req_headers.update(headers)

        try:
            async with self._timeout_ctx_factory(self.timeout):
                async with await self._make_request(
                    method, url, headers=req_headers, params=params, json=json
                ) as response:
                    if response.status == 401:
                        raise SequenceAuthError("Invalid access token")

                    if response.status not in (200, 201, 202):
                        try:
                            err_data = await response.json()
                            err_msg = err_data.get("error", {}).get("message", "")
                            err_code = err_data.get("error", {}).get("code", "")
                            if err_msg:
                                msg = f"{err_code}: {err_msg}" if err_code else err_msg
                            else:
                                msg = f"API request failed with status {response.status}"
                        except Exception:
                            msg = f"API request failed with status {response.status}"
                        raise SequenceApiError(msg)

                    data = await response.json()
                    _LOGGER.debug("API Response from %s: %s", url, data)

                    if isinstance(data, dict) and "data" in data:
                        return data["data"]
                    return data
        except TimeoutError as err:
            raise SequenceConnectionError(
                "Timeout while connecting to Sequence API"
            ) from err
        except aiohttp.ClientError as err:
            raise SequenceConnectionError(
                f"Failed to connect to Sequence API: {err}"
            ) from err

    async def _async_get_all_pages(self, url: str, params: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Automatically traverse and fetch all pages of a paginated list endpoint."""
        if "page" in params:
            data = await self._async_request("GET", url, params=params)
            if isinstance(data, dict) and "items" in data:
                return data["items"]
            return data if isinstance(data, list) else []

        all_items: List[Dict[str, Any]] = []
        page = 1
        page_size = 100
        current_params = dict(params)
        current_params["pageSize"] = page_size

        while True:
            current_params["page"] = page
            data = await self._async_request("GET", url, params=current_params)

            items = []
            pagination = {}
            if isinstance(data, dict):
                items = data.get("items", [])
                pagination = data.get("pagination", {})
            elif isinstance(data, list):
                items = data

            all_items.extend(items)
            if not pagination.get("hasNextPage", False) or not items:
                break
            page += 1

        return all_items
