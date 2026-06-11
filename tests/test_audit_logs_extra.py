"""Tests for AuditLogsService list behavior and model mapping."""

import pytest
from GetSequenceIoApiClient.client import SequenceApiClient
from tests.test_client import DummyResponse, DummySession
from GetSequenceIoApiClient import models


@pytest.mark.asyncio
async def test_async_list_audit_logs_params_and_models():
    log = {
        "id": "log1",
        "createdAt": "2024-01-01T00:00:00Z",
        "apiKeyId": "k1",
        "apiKeyName": "k",
        "path": "/accounts",
        "action": "LIST_ACCOUNTS",
        "requestId": "req1",
        "outcome": "SUCCESS",
    }
    resp = DummyResponse(200, {"items": [log], "pagination": {"page": 1, "pageSize": 10, "hasNextPage": False}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    logs = await client.async_list_audit_logs(api_key_id="k1", action="LIST_ACCOUNTS")
    # verify params encoded
    params = session.last_request["params"]
    assert params.get("apiKeyId") == "k1"
    assert params.get("action") == "LIST_ACCOUNTS"
    assert isinstance(logs[0], models.AuditLogEntry)


@pytest.mark.asyncio
async def test_async_list_audit_logs_pagination_concat():
    log1 = {"id": "l1", "createdAt": "2024-01-01T00:00:00Z", "apiKeyId": "k1", "apiKeyName": "k", "path": "/x", "action": "A", "requestId": "r1", "outcome": "SUCCESS"}
    log2 = {"id": "l2", "createdAt": "2024-01-02T00:00:00Z", "apiKeyId": "k1", "apiKeyName": "k", "path": "/x", "action": "A", "requestId": "r2", "outcome": "SUCCESS"}
    resp1 = DummyResponse(200, {"items": [log1], "pagination": {"page": 1, "pageSize": 1, "hasNextPage": True}})
    resp2 = DummyResponse(200, {"items": [log2], "pagination": {"page": 2, "pageSize": 1, "hasNextPage": False}})
    session = DummySession([resp1, resp2])
    client = SequenceApiClient(session, "token")
    results = await client.async_list_audit_logs()
    assert len(results) == 2
