"""Additional tests targeting ActivityService behaviors."""

import pytest
from GetSequenceIoApiClient.client import SequenceApiClient, SequenceApiError
from tests.test_client import DummyResponse, DummySession
from GetSequenceIoApiClient import models


@pytest.mark.asyncio
async def test_async_list_transfers_by_account_params_and_models():
    item = {"id": "t_by_acc", "amountInCents": 150, "direction": "INTERNAL", "origin": "RULE", "source": None, "destination": None, "status": "COMPLETE", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z"}
    resp = DummyResponse(200, {"items": [item], "pagination": {"page": 1, "pageSize": 10, "hasNextPage": False}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    results = await client.async_list_transfers_by_account("acc1", account_role="SOURCE")
    # verify request params encoded correctly
    assert session.last_request["params"].get("accountRole") == "SOURCE"
    assert isinstance(results[0], models.Transfer)


@pytest.mark.asyncio
async def test_async_list_card_transactions_page_param_returns_one():
    card_item = {"id": "c_t1", "cardId": "card1", "cardType": "DEBIT_CARD", "account": {"id": "a1", "name": "n", "type": "POD", "isDeleted": False}, "direction": "MONEY_OUT", "subtype": "PURCHASE", "status": "COMPLETE", "amountInCents": 4250, "description": "Coffee", "createdAt": "2024-01-01T00:00:00Z", "completedAt": "2024-01-01T00:00:00Z"}
    resp = DummyResponse(200, {"items": [card_item], "pagination": {"page": 1, "pageSize": 10, "hasNextPage": False}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    cards = await client.async_list_card_transactions(page=1)
    assert len(cards) == 1


@pytest.mark.asyncio
async def test_async_create_transfer_raises_api_error_on_500():
    resp = DummyResponse(500, {"error": {"message": "boom", "code": "X"}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    with pytest.raises(SequenceApiError):
        await client.async_create_transfer("s", "d", 1000)
