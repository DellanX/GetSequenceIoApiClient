"""Shared base client utilities (HTTP request and pagination)."""
from __future__ import annotations

import asyncio
import logging
from contextlib import asynccontextmanager
from typing import Optional, Callable, AsyncContextManager, cast

import aiohttp
import inspect
from pydantic import ValidationError

from .config import SequenceClientConfig
from ._types import ApiErrorResponse, Headers, JsonObject, JsonValue, PaginatedResponse, QueryParams
from .exceptions import (
    SequenceApiError,
    SequenceAuthError,
    SequenceConnectionError,
)

API_BASE_URL = "https://api.getsequence.io/platform/v1"
API_TIMEOUT = 30

_LOGGER = logging.getLogger(__name__)


@asynccontextmanager
async def _default_timeout_ctx(timeout_seconds: int):
    # Python 3.11+ has asyncio.timeout; Python 3.10 needs a fallback.
    if hasattr(asyncio, "timeout"):
        async with asyncio.timeout(timeout_seconds):
            yield
        return

    task = asyncio.current_task()
    if task is None:
        raise RuntimeError("No current asyncio task for timeout context")

    timeout_handle = asyncio.get_running_loop().call_later(timeout_seconds, task.cancel)
    try:
        yield
    except asyncio.CancelledError as err:
        raise TimeoutError("Operation timed out") from err
    finally:
        timeout_handle.cancel()


class BaseClient:
    """Encapsulates HTTP request logic and pagination helpers."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        access_token: str,
        *,
        config: Optional[SequenceClientConfig] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        request_factory: Optional[Callable[..., AsyncContextManager]] = None,
        timeout_ctx_factory: Optional[Callable[[int], AsyncContextManager]] = None,
    ) -> None:
        self.session = session
        self.access_token = access_token
        resolved_base_url = base_url if base_url is not None else API_BASE_URL
        resolved_timeout = timeout if timeout is not None else API_TIMEOUT
        try:
            resolved_config = config or SequenceClientConfig(
                base_url=resolved_base_url,
                timeout_seconds=resolved_timeout,
            )
        except ValidationError as err:
            raise ValueError(f"Invalid Sequence client configuration: {err}") from err

        self.base_url = resolved_config.base_url
        # make timeout injectable for tests
        self.timeout = resolved_config.timeout_seconds

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
            else _default_timeout_ctx
        )

    async def _make_request(
        self,
        method: str,
        url: str,
        headers: Headers,
        params: Optional[QueryParams],
        json: Optional[JsonObject],
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
        headers: Optional[Headers] = None,
        params: Optional[QueryParams] = None,
        json: Optional[JsonObject] = None,
    ) -> JsonValue:
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
                            err_data = cast(ApiErrorResponse, await response.json())
                            err_msg = err_data.get("error", {}).get("message", "")
                            err_code = err_data.get("error", {}).get("code", "")
                            if err_msg:
                                msg = f"{err_code}: {err_msg}" if err_code else err_msg
                            else:
                                msg = f"API request failed with status {response.status}"
                        except Exception:
                            msg = f"API request failed with status {response.status}"
                        raise SequenceApiError(msg)

                    data = cast(JsonValue, await response.json())
                    _LOGGER.debug("API Response from %s: %s", url, data)

                    if isinstance(data, dict) and "data" in data:
                        return cast(JsonValue, data["data"])
                    return data
        except TimeoutError as err:
            raise SequenceConnectionError(
                "Timeout while connecting to Sequence API"
            ) from err
        except aiohttp.ClientError as err:
            raise SequenceConnectionError(
                f"Failed to connect to Sequence API: {err}"
            ) from err

    async def _async_get_all_pages(self, url: str, params: QueryParams) -> list[JsonObject]:
        """Automatically traverse and fetch all pages of a paginated list endpoint."""
        if "page" in params:
            data = await self._async_request("GET", url, params=params)
            if isinstance(data, dict) and "items" in data:
                items = cast(list[JsonObject], data["items"])
                return items
            return cast(list[JsonObject], data) if isinstance(data, list) else []

        all_items: list[JsonObject] = []
        page = 1
        page_size = 100
        current_params = dict(params)
        current_params["pageSize"] = page_size

        while True:
            current_params["page"] = page
            data = await self._async_request("GET", url, params=current_params)

            items: list[JsonObject] = []
            pagination: dict[str, JsonValue] = {}
            if isinstance(data, dict):
                paginated = cast(PaginatedResponse, data)
                items = paginated.get("items", [])
                pagination = cast(dict[str, JsonValue], paginated.get("pagination", {}))
            elif isinstance(data, list):
                items = cast(list[JsonObject], data)

            all_items.extend(items)
            if not pagination.get("hasNextPage", False) or not items:
                break
            page += 1

        return all_items
