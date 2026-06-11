"""Extra tests targeting AccountsService behaviors."""

import pytest
from GetSequenceIoApiClient.client import SequenceApiClient
from tests.test_client import DummyResponse, DummySession


@pytest.mark.asyncio
async def test_async_get_accounts_multiple_pages():
    a1 = {"id": "a1", "name": "A1", "type": "POD"}
    a2 = {"id": "a2", "name": "A2", "type": "POD"}
    resp1 = DummyResponse(200, {"items": [a1], "pagination": {"page": 1, "pageSize": 1, "hasNextPage": True}})
    resp2 = DummyResponse(200, {"items": [a2], "pagination": {"page": 2, "pageSize": 1, "hasNextPage": False}})
    session = DummySession([resp1, resp2])
    client = SequenceApiClient(session, "token")
    results = await client.async_get_accounts()
    assert len(results) == 2


@pytest.mark.asyncio
async def test_async_get_accounts_filters_params():
    resp = DummyResponse(200, {"items": [], "pagination": {"page": 1, "pageSize": 10, "hasNextPage": False}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    await client.async_get_accounts(type="Pod", state="ACTIVE", page=1, page_size=5)
    params = session.last_request["params"]
    assert params.get("type") == "Pod"
    assert params.get("state") == "ACTIVE"
    assert params.get("page") == 1
    assert params.get("pageSize") == 5
