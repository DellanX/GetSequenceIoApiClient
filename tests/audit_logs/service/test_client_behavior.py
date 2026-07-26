import pytest
from GetSequenceIoApiClient.client import SequenceApiClient
from tests._dummy_client import DummyResponse, DummySession
from GetSequenceIoApiClient import models


@pytest.mark.asyncio
async def test_external_and_card_and_audit_endpoints():
    ext_tx = {"id": "x1", "accountId": "a1", "amountInCents": 4200, "direction": "MONEY_OUT", "status": "COMPLETE", "description": "X", "transactionDate": "2024-01-01"}
    card_tx = {"id": "c1", "cardId": "card1", "cardType": "DEBIT_CARD", "account": {"id": "a1", "name": "n", "type": "POD", "isDeleted": False}, "direction": "MONEY_OUT", "subtype": "PURCHASE", "status": "COMPLETE", "amountInCents": 4250, "description": "Coffee", "createdAt": "2024-01-01T00:00:00Z", "completedAt": "2024-01-01T00:00:00Z"}
    audit = {"id": "log1", "createdAt": "2024-01-01T00:00:00Z", "apiKeyId": "k1", "apiKeyName": "k", "path": "/accounts", "action": "LIST_ACCOUNTS", "requestId": "req1", "outcome": "SUCCESS"}
    session = DummySession([DummyResponse(200, {"items": [ext_tx], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}), DummyResponse(200, {"items": [card_tx], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}), DummyResponse(200, {"items": [audit], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}})])
    client = SequenceApiClient(session, "token")
    exs = await client.activity.async_list_external_transactions()
    assert isinstance(exs[0], models.ExternalTransaction)
    cards = await client.activity.async_list_card_transactions()
    assert isinstance(cards[0], models.Transaction)
    logs = await client.audit_logs.async_list_audit_logs()
    assert isinstance(logs[0], models.AuditLogEntry)


@pytest.mark.asyncio
async def test_audit_logs_params_and_pagination():
    audit = {"id": "log1", "createdAt": "2024-01-01T00:00:00Z", "apiKeyId": "k1", "apiKeyName": "k", "path": "/accounts", "action": "LIST_ACCOUNTS", "requestId": "req1", "outcome": "SUCCESS"}
    resp = DummyResponse(200, {"items": [audit], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    logs = await client.audit_logs.async_list_audit_logs(api_key_id="k1", action="LIST_ACCOUNTS", from_date="2024-01-01", to_date="2024-01-02", page=1, page_size=10)
    assert session.last_request["params"]["apiKeyId"] == "k1"
    assert isinstance(logs[0], models.AuditLogEntry)
