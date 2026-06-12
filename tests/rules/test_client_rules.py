import pytest
from GetSequenceIoApiClient.client import SequenceApiClient
from tests._dummy_client import DummyResponse, DummySession
from GetSequenceIoApiClient import models


@pytest.mark.asyncio
async def test_rules_endpoints_and_trigger():
    rule_summary = {"id": "r1", "name": "r", "status": "ENABLED", "isSupported": True, "createdAt": "2024-01-01T00:00:00Z"}
    rule_detail = {"id": "r1", "name": "r", "status": "ENABLED", "steps": [], "createdAt": "2024-01-01T00:00:00Z"}
    trigger_resp = {"executionId": "exec1"}
    session = DummySession([DummyResponse(200, {"items": [rule_summary], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}), DummyResponse(200, rule_detail), DummyResponse(202, trigger_resp)])
    client = SequenceApiClient(session, "token")
    rules = await client.rules.async_list_rules()
    assert isinstance(rules[0], models.RuleSummary)
    rule = await client.rules.async_get_rule("r1")
    assert isinstance(rule, models.Rule)
    exec_id = await client.rules.async_trigger_rule("r1", execute_amount=100, simulation=True)
    assert exec_id == "exec1"


@pytest.mark.asyncio
async def test_rule_executions_get():
    exec_summary = {"id": "e1", "ruleId": "r1", "status": "EXECUTED", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z"}
    exec_detail = {"id": "e1", "ruleId": "r1", "status": "EXECUTED", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z", "transferIds": []}
    session = DummySession([DummyResponse(200, {"items": [exec_summary], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}), DummyResponse(200, exec_detail)])
    client = SequenceApiClient(session, "token")
    exs = await client.rules.async_list_rule_executions("r1")
    assert isinstance(exs[0], models.RuleExecutionSummary)
    ex = await client.rules.async_get_rule_execution("r1", "e1")
    assert isinstance(ex, models.RuleExecution)
