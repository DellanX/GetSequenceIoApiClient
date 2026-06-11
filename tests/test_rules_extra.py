"""Extra tests for RulesService behaviors."""

import pytest
from GetSequenceIoApiClient.client import SequenceApiClient
from tests.test_client import DummyResponse, DummySession
from GetSequenceIoApiClient import models


@pytest.mark.asyncio
async def test_async_list_rules_and_get_rule():
    summary = {"id": "r1", "name": "Rule 1", "status": "ENABLED", "isSupported": True, "createdAt": "2024-01-01T00:00:00Z"}
    detail = {"id": "r1", "name": "Rule 1", "status": "ENABLED", "steps": [], "createdAt": "2024-01-01T00:00:00Z"}
    session = DummySession([DummyResponse(200, {"items": [summary], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}), DummyResponse(200, detail)])
    client = SequenceApiClient(session, "token")
    rules = await client.async_list_rules()
    assert isinstance(rules[0], models.RuleSummary)
    r = await client.async_get_rule("r1")
    assert isinstance(r, models.Rule)


@pytest.mark.asyncio
async def test_async_trigger_rule_returns_execution_id():
    trigger_resp = {"executionId": "exec-123"}
    session = DummySession([DummyResponse(202, trigger_resp)])
    client = SequenceApiClient(session, "token")
    exec_id = await client.async_trigger_rule("r1", execute_amount=50, simulation=True, idempotency_key="k")
    # verify header was set
    assert exec_id == "exec-123"
    assert session.last_request["headers"].get("idempotency-key") == "k"


@pytest.mark.asyncio
async def test_async_list_rule_executions_pagination_and_get():
    s1 = {"id": "e1", "ruleId": "r1", "status": "EXECUTED", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z"}
    d1 = {"id": "e1", "ruleId": "r1", "status": "EXECUTED", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z", "transferIds": []}
    resp1 = DummyResponse(200, {"items": [s1], "pagination": {"page":1,"pageSize":1,"hasNextPage": True}})
    resp2 = DummyResponse(200, {"items": [], "pagination": {"page":2,"pageSize":1,"hasNextPage": False}})
    session = DummySession([resp1, resp2, DummyResponse(200, d1)])
    client = SequenceApiClient(session, "token")
    exs = await client.async_list_rule_executions("r1")
    assert isinstance(exs[0], models.RuleExecutionSummary)
    ex = await client.async_get_rule_execution("r1", "e1")
    assert isinstance(ex, models.RuleExecution)


@pytest.mark.asyncio
async def test_async_list_rules_filters_params():
    resp = DummyResponse(200, {"items": [], "pagination": {"page":1,"pageSize":10,"hasNextPage": False}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    await client.async_list_rules(source_id="s-1", page=1, page_size=5)
    params = session.last_request["params"]
    assert params.get("sourceId") == "s-1"
    assert params.get("page") == 1
    assert params.get("pageSize") == 5
