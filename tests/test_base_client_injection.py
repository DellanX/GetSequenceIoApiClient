"""Tests exercising BaseClient using injected factories for requests and timeouts."""

import asyncio
import aiohttp
import pytest

from GetSequenceIoApiClient import _base
from GetSequenceIoApiClient.exceptions import SequenceConnectionError


class FakeTimeoutCtx:
    def __init__(self, raise_on_enter: bool = True):
        self.raise_on_enter = raise_on_enter

    async def __aenter__(self):
        if self.raise_on_enter:
            raise TimeoutError("timed out")
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class Resp:
    def __init__(self, status: int, data):
        self.status = status
        self._data = data

    async def json(self):
        return self._data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


@pytest.mark.asyncio
async def test_timeout_ctx_factory_raises_sequence_connection_error():
    # Use a timeout_ctx_factory that raises TimeoutError on enter
    session = type("S", (), {"request": lambda *a, **k: Resp(200, {})})()
    client = _base.BaseClient(session, "token", timeout_ctx_factory=lambda t: FakeTimeoutCtx(True))

    with pytest.raises(SequenceConnectionError):
        await client._async_request("GET", "http://example")


@pytest.mark.asyncio
async def test_request_factory_raises_clienterror_translates_to_sequence_connection_error():
    # Provide a request_factory that raises aiohttp.ClientError when awaited
    async def bad_req(*a, **k):
        raise aiohttp.ClientError("connect failed")

    client = _base.BaseClient(None, "token", request_factory=bad_req)

    with pytest.raises(SequenceConnectionError):
        await client._async_request("GET", "http://example")


@pytest.mark.asyncio
async def test_async_get_all_pages_with_injected_request_factory_paginates():
    # Simulate two pages: page 1 hasNextPage True, page 2 hasNextPage False
    def factory(method, url, headers=None, params=None, json=None):
        p = (params or {}).get("page", 1)
        data = {"items": [{"id": f"p{p}"}], "pagination": {"hasNextPage": p < 2}}
        return Resp(200, data)

    client = _base.BaseClient(None, "token", request_factory=factory)
    items = await client._async_get_all_pages("http://example", {})
    assert isinstance(items, list)
    assert {it["id"] for it in items} == {"p1", "p2"}
