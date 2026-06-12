"""Tests for BaseClient error handling: timeouts and connection errors."""

import asyncio
import pytest
import aiohttp

from GetSequenceIoApiClient import _base
from GetSequenceIoApiClient.exceptions import SequenceConnectionError, SequenceAuthError, SequenceApiError
from tests._dummy_client import DummyResponse, DummySession


class SlowResponse:
    def __init__(self, json_data=None):
        self._json_data = json_data

    async def json(self):
        return self._json_data

    async def __aenter__(self):
        # sleep long enough to trigger the module timeout (we patch API_TIMEOUT in tests)
        await asyncio.sleep(_base.API_TIMEOUT + 0.01)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class SlowSession:
    def request(self, *args, **kwargs):
        return SlowResponse({})


class SlowResponseTimeout:
    async def __aenter__(self):
        raise TimeoutError("timed out")

    async def __aexit__(self, exc_type, exc, tb):
        return False


class BadSession:
    def request(self, *args, **kwargs):
        raise aiohttp.ClientError("connect failed")


@pytest.mark.asyncio
async def test_timeout_raises_sequence_connection_error():
    # Use injectable timeout context factory to force a TimeoutError
    base = _base.BaseClient(SlowSession(), "token", timeout_ctx_factory=lambda t: SlowResponseTimeout())

    with pytest.raises(SequenceConnectionError):
        await base._async_request("GET", "http://example")


@pytest.mark.asyncio
async def test_aiohttp_clienterror_raises_sequence_connection_error():
    base = _base.BaseClient(BadSession(), "token")
    # patch _make_request to raise ClientError when awaited
    async def make_req(*a, **k):
        raise aiohttp.ClientError("connect failed")

    base._make_request = make_req
    with pytest.raises(SequenceConnectionError):
        await base._async_request("GET", "http://example")


@pytest.mark.asyncio
async def test_401_raises_sequence_auth_error():
    resp = DummyResponse(401, {})
    session = type("S", (), {"request": lambda *a, **k: resp})()
    base = _base.BaseClient(session, "token")
    with pytest.raises(SequenceAuthError):
        await base._async_request("GET", "http://example")


@pytest.mark.asyncio
async def test_500_without_body_raises_sequence_api_error():
    resp = DummyResponse(500, None)
    session = type("S", (), {"request": lambda *a, **k: resp})()
    base = _base.BaseClient(session, "token")
    with pytest.raises(SequenceApiError):
        await base._async_request("GET", "http://example")


@pytest.mark.asyncio
async def test_500_with_error_body_includes_code_and_message():
    body = {"error": {"message": "boom", "code": "X123"}}
    resp = DummyResponse(500, body)
    session = type("S", (), {"request": lambda *a, **k: resp})()
    base = _base.BaseClient(session, "token")
    with pytest.raises(SequenceApiError) as exc:
        await base._async_request("GET", "http://example")
    assert "X123: boom" in str(exc.value)


class BadJsonResponse:
    def __init__(self, status=500):
        self.status = status

    async def json(self):
        raise RuntimeError("no json")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


@pytest.mark.asyncio
async def test_500_with_json_error_uses_generic_message():
    resp = BadJsonResponse(500)
    session = type("S", (), {"request": lambda *a, **k: resp})()
    base = _base.BaseClient(session, "token")
    with pytest.raises(SequenceApiError) as exc:
        await base._async_request("GET", "http://example")
    assert "API request failed with status 500" in str(exc.value)


@pytest.mark.asyncio
async def test_async_get_all_pages_handles_list_results():
    # craft a plain-list JSON response to exercise the 'elif isinstance(data, list)' branch
    item = {"id": "t1", "amountInCents": 100, "direction": "INTERNAL", "origin": "RULE", "source": None, "destination": None, "status": "COMPLETE", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z"}
    resp = DummyResponse(200, [item])
    session = DummySession(resp)
    from GetSequenceIoApiClient.client import SequenceApiClient
    client = SequenceApiClient(session, "token")
    results = await client.activity.async_list_transfers()
    assert isinstance(results, list)


@pytest.mark.asyncio
async def test_headers_merge_executes_update():
    # ensure that passing headers into _async_request triggers the update branch
    resp = DummyResponse(200, {})
    def req(*a, **k):
        # assert that merged headers contain our custom header
        headers = k.get("headers") or (a[2] if len(a) > 2 else {})
        assert headers.get("X-Test") == "1"
        return resp

    session = type("S", (), {"request": req})()
    base = _base.BaseClient(session, "token")
    await base._async_request("GET", "http://example", headers={"X-Test": "1"})


@pytest.mark.asyncio
async def test_500_with_error_message_no_code_uses_message_only():
    body = {"error": {"message": "onlymsg"}}
    resp = DummyResponse(500, body)
    session = type("S", (), {"request": lambda *a, **k: resp})()
    base = _base.BaseClient(session, "token")
    with pytest.raises(SequenceApiError) as exc:
        await base._async_request("GET", "http://example")
    assert "onlymsg" in str(exc.value)


@pytest.mark.asyncio
async def test_500_with_no_error_field_uses_status_message():
    body = {"other": "x"}
    resp = DummyResponse(500, body)
    session = type("S", (), {"request": lambda *a, **k: resp})()
    base = _base.BaseClient(session, "token")
    with pytest.raises(SequenceApiError) as exc:
        await base._async_request("GET", "http://example")
    assert "API request failed with status 500" in str(exc.value)


@pytest.mark.asyncio
async def test_async_get_all_pages_with_page_param_returns_items():
    # When 'page' is in params, should return items directly
    data = {"items": [{"id": "x"}]}
    resp = DummyResponse(200, data)
    session = DummySession(resp)
    base = _base.BaseClient(session, "token")
    items = await base._async_get_all_pages("http://example", {"page": 1})
    assert isinstance(items, list)


@pytest.mark.asyncio
async def test_async_get_all_pages_with_page_param_and_list_response():
    # When params contains 'page' and the returned data is a list, ensure it returns the list
    resp = DummyResponse(200, [{"id": "x1"}, {"id": "x2"}])
    session = DummySession(resp)
    base = _base.BaseClient(session, "token")
    res = await base._async_get_all_pages("http://example", {"page": 1})
    assert isinstance(res, list)
    assert {r["id"] for r in res} == {"x1", "x2"}
