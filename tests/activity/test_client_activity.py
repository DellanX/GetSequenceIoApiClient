import pytest
from GetSequenceIoApiClient.client import SequenceApiClient
from GetSequenceIoApiClient import models
from tests._dummy_client import DummyResponse, DummySession


@pytest.mark.asyncio
async def test_list_transfers_and_accountids_encoding():
    transfer_item = {
        "id": "t1",
        "amountInCents": 100,
        "direction": "INTERNAL",
        "origin": "RULE",
        "source": {"id": "s1", "name": "S", "type": "POD", "isDeleted": False},
        "destination": {"id": "d1", "name": "D", "type": "POD", "isDeleted": False},
        "status": "COMPLETE",
        "executionMode": "LIVE",
        "createdAt": "2024-01-01T00:00:00Z",
    }
    dummy_response = DummyResponse(200, {"items": [transfer_item], "pagination": {"page": 1, "pageSize": 10, "hasNextPage": False}})
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "token")
    transfers = await client.activity.async_list_transfers(account_ids=["s1", "d1"])
    assert isinstance(session.last_request["params"].get("accountIds"), list)
    assert isinstance(transfers, list)
    assert isinstance(transfers[0], models.Transfer)


@pytest.mark.asyncio
async def test_list_transfers_pagination():
    item1 = {"id": "t1", "amountInCents": 100, "direction": "INTERNAL", "origin": "RULE", "source": None, "destination": None, "status": "COMPLETE", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z"}
    item2 = {"id": "t2", "amountInCents": 200, "direction": "INTERNAL", "origin": "RULE", "source": None, "destination": None, "status": "COMPLETE", "executionMode": "LIVE", "createdAt": "2024-01-02T00:00:00Z"}
    resp1 = DummyResponse(200, {"items": [item1], "pagination": {"page": 1, "pageSize": 1, "hasNextPage": True}})
    resp2 = DummyResponse(200, {"items": [item2], "pagination": {"page": 2, "pageSize": 1, "hasNextPage": False}})
    session = DummySession([resp1, resp2])
    client = SequenceApiClient(session, "token")
    results = await client.activity.async_list_transfers()
    assert len(results) == 2


@pytest.mark.asyncio
async def test_list_transfers_single_page_param():
    item = {"id": "t_single", "amountInCents": 50, "direction": "INTERNAL", "origin": "RULE", "source": None, "destination": None, "status": "COMPLETE", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z"}
    resp = DummyResponse(200, {"items": [item], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    res = await client.activity.async_list_transfers(page=1)
    assert len(res) == 1


@pytest.mark.asyncio
async def test_create_and_get_transfer():
    create_payload = {"id": "new", "amountInCents": 5000, "direction": "MONEY_OUT", "origin": "USER", "source": None, "destination": None, "status": "PROCESSING", "executionMode": "LIVE", "createdAt": "2024-01-03T00:00:00Z"}
    session = DummySession([DummyResponse(201, create_payload), DummyResponse(200, create_payload)])
    client = SequenceApiClient(session, "token")
    created = await client.activity.async_create_transfer("s", "d", 5000)
    assert isinstance(created, models.Transfer)
    fetched = await client.activity.async_get_transfer("new")
    assert fetched.id == "new"
