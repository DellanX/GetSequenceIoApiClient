import pytest

from GetSequenceIoApiClient import models
from GetSequenceIoApiClient.activity import ActivityService
from GetSequenceIoApiClient.client import SequenceApiClient
from tests._dummy_client import DummyResponse, DummySession


def _require_method(service_cls, method_name: str):
    method = getattr(service_cls, method_name, None)
    if method is None:
        pytest.skip(f"{service_cls.__name__}.{method_name} is not implemented yet")
    return method


@pytest.mark.asyncio
async def test_async_get_card_transaction_returns_transaction_model():
    _require_method(ActivityService, "async_get_card_transaction")
    payload = {
        "id": "c1",
        "cardId": "card1",
        "cardType": "DEBIT_CARD",
        "account": {"id": "a1", "name": "n", "type": "POD", "isDeleted": False},
        "direction": "MONEY_OUT",
        "subtype": "PURCHASE",
        "status": "COMPLETE",
        "amountInCents": 4250,
        "description": "Coffee",
        "createdAt": "2024-01-01T00:00:00Z",
        "completedAt": "2024-01-01T00:00:00Z",
    }
    session = DummySession(DummyResponse(200, payload))
    client = SequenceApiClient(session, "token")

    tx = await client.activity.async_get_card_transaction("c1")
    assert isinstance(tx, models.Transaction)
    assert session.last_request["url"].endswith("/card-transactions/c1")


@pytest.mark.asyncio
async def test_async_get_external_transaction_returns_external_transaction_model():
    _require_method(ActivityService, "async_get_external_transaction")
    payload = {
        "id": "x1",
        "accountId": "a1",
        "amountInCents": 4200,
        "direction": "MONEY_OUT",
        "status": "COMPLETE",
        "description": "X",
        "transactionDate": "2024-01-01",
    }
    session = DummySession(DummyResponse(200, payload))
    client = SequenceApiClient(session, "token")

    tx = await client.activity.async_get_external_transaction("x1")
    assert isinstance(tx, models.ExternalTransaction)
    assert session.last_request["url"].endswith("/external-transactions/x1")
