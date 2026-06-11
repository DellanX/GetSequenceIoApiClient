"""Minimal async tests for OpenAPI-backed SequenceApiClient."""

import pytest
from GetSequenceIoApiClient.client import (
    SequenceApiClient,
    SequenceApiError,
    SequenceAuthError,
)
from GetSequenceIoApiClient import models


class DummyResponse:
    def __init__(self, status, json_data):
        self.status = status
        self._json_data = json_data

    async def json(self):
        return self._json_data

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class DummySession:
    def __init__(self, response):
        # response can be a single DummyResponse or an iterable of DummyResponse
        if isinstance(response, list):
            self._responses = list(response)
        else:
            self._responses = [response]
        self.last_request = None

    def request(self, method, url, headers=None, params=None, json=None):
        self.last_request = {"method": method, "url": url, "headers": headers, "params": params, "json": json}
        if not self._responses:
            # default empty 200
            return DummyResponse(200, {})
        return self._responses.pop(0)


@pytest.mark.asyncio
async def test_async_get_accounts_success():
    accounts_data = {"data": {"accounts": []}}
    dummy_response = DummyResponse(200, accounts_data)
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "test-token")
    result = await client.async_get_accounts()
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_async_get_accounts_auth_error():
    dummy_response = DummyResponse(401, {})
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "bad-token")
    with pytest.raises(SequenceAuthError):
        await client.async_get_accounts()


@pytest.mark.asyncio
async def test_async_get_accounts_api_error():
    dummy_response = DummyResponse(500, {})
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "test-token")
    with pytest.raises(SequenceApiError):
        await client.async_get_accounts()


@pytest.mark.asyncio
async def test_async_test_connection_success():
    accounts_data = {"data": {"accounts": []}}
    dummy_response = DummyResponse(200, accounts_data)
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "test-token")
    assert await client.async_test_connection() is True


@pytest.mark.asyncio
async def test_async_test_connection_failure():
    dummy_response = DummyResponse(401, {})
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "bad-token")
    assert await client.async_test_connection() is False


@pytest.mark.asyncio
async def test_async_get_account_and_models():
    # Test GET /accounts/{id} returns Account model
    account_payload = {
        "id": "a1",
        "name": "Acct",
        "type": "POD",
        "balance": {"balanceInCents": 12345, "error": None},
    }
    dummy_response = DummyResponse(200, account_payload)
    session = DummySession(dummy_response)
    client = SequenceApiClient(session, "token")
    acct = await client.async_get_account("a1")
    assert isinstance(acct, models.Account)
    assert acct.balance.balance_in_cents == 12345


@pytest.mark.asyncio
async def test_list_transfers_and_accountids_encoding():
    # Ensure accountIds are sent as list and transfers return Transfer models
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
    transfers = await client.async_list_transfers(account_ids=["s1", "d1"])
    # verify request params encoded as list
    assert isinstance(session.last_request["params"].get("accountIds"), list)
    assert isinstance(transfers, list)
    assert isinstance(transfers[0], models.Transfer)


@pytest.mark.asyncio
async def test_list_transfers_pagination():
    # Two page responses must be concatenated
    item1 = {"id": "t1", "amountInCents": 100, "direction": "INTERNAL", "origin": "RULE", "source": None, "destination": None, "status": "COMPLETE", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z"}
    item2 = {"id": "t2", "amountInCents": 200, "direction": "INTERNAL", "origin": "RULE", "source": None, "destination": None, "status": "COMPLETE", "executionMode": "LIVE", "createdAt": "2024-01-02T00:00:00Z"}
    resp1 = DummyResponse(200, {"items": [item1], "pagination": {"page": 1, "pageSize": 1, "hasNextPage": True}})
    resp2 = DummyResponse(200, {"items": [item2], "pagination": {"page": 2, "pageSize": 1, "hasNextPage": False}})
    session = DummySession([resp1, resp2])
    client = SequenceApiClient(session, "token")
    results = await client.async_list_transfers()
    assert len(results) == 2


@pytest.mark.asyncio
async def test_list_transfers_single_page_param():
    item = {"id": "t_single", "amountInCents": 50, "direction": "INTERNAL", "origin": "RULE", "source": None, "destination": None, "status": "COMPLETE", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z"}
    resp = DummyResponse(200, {"items": [item], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    res = await client.async_list_transfers(page=1)
    assert len(res) == 1


@pytest.mark.asyncio
async def test_create_and_get_transfer():
    create_payload = {"id": "new", "amountInCents": 5000, "direction": "MONEY_OUT", "origin": "USER", "source": None, "destination": None, "status": "PROCESSING", "executionMode": "LIVE", "createdAt": "2024-01-03T00:00:00Z"}
    session = DummySession([DummyResponse(201, create_payload), DummyResponse(200, create_payload)])
    client = SequenceApiClient(session, "token")
    created = await client.async_create_transfer("s", "d", 5000)
    assert isinstance(created, models.Transfer)
    fetched = await client.async_get_transfer("new")
    assert fetched.id == "new"


@pytest.mark.asyncio
async def test_rules_endpoints_and_trigger():
    rule_summary = {"id": "r1", "name": "r", "status": "ENABLED", "isSupported": True, "createdAt": "2024-01-01T00:00:00Z"}
    rule_detail = {"id": "r1", "name": "r", "status": "ENABLED", "steps": [], "createdAt": "2024-01-01T00:00:00Z"}
    trigger_resp = {"executionId": "exec1"}
    session = DummySession([DummyResponse(200, {"items": [rule_summary], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}), DummyResponse(200, rule_detail), DummyResponse(202, trigger_resp)])
    client = SequenceApiClient(session, "token")
    rules = await client.async_list_rules()
    assert isinstance(rules[0], models.RuleSummary)
    rule = await client.async_get_rule("r1")
    assert isinstance(rule, models.Rule)
    exec_id = await client.async_trigger_rule("r1", execute_amount=100, simulation=True)
    assert exec_id == "exec1"


@pytest.mark.asyncio
async def test_rule_executions_get():
    exec_summary = {"id": "e1", "ruleId": "r1", "status": "EXECUTED", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z"}
    exec_detail = {"id": "e1", "ruleId": "r1", "status": "EXECUTED", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z", "transferIds": []}
    session = DummySession([DummyResponse(200, {"items": [exec_summary], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}), DummyResponse(200, exec_detail)])
    client = SequenceApiClient(session, "token")
    exs = await client.async_list_rule_executions("r1")
    assert isinstance(exs[0], models.RuleExecutionSummary)
    ex = await client.async_get_rule_execution("r1", "e1")
    assert isinstance(ex, models.RuleExecution)


@pytest.mark.asyncio
async def test_external_and_card_and_audit_endpoints():
    ext_tx = {"id": "x1", "accountId": "a1", "amountInCents": 4200, "direction": "MONEY_OUT", "status": "COMPLETE", "description": "X", "transactionDate": "2024-01-01"}
    card_tx = {"id": "c1", "cardId": "card1", "cardType": "DEBIT_CARD", "account": {"id": "a1", "name": "n", "type": "POD", "isDeleted": False}, "direction": "MONEY_OUT", "subtype": "PURCHASE", "status": "COMPLETE", "amountInCents": 4250, "description": "Coffee", "createdAt": "2024-01-01T00:00:00Z", "completedAt": "2024-01-01T00:00:00Z"}
    audit = {"id": "log1", "createdAt": "2024-01-01T00:00:00Z", "apiKeyId": "k1", "apiKeyName": "k", "path": "/accounts", "action": "LIST_ACCOUNTS", "requestId": "req1", "outcome": "SUCCESS"}
    session = DummySession([DummyResponse(200, {"items": [ext_tx], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}), DummyResponse(200, {"items": [card_tx], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}), DummyResponse(200, {"items": [audit], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}})])
    client = SequenceApiClient(session, "token")
    exs = await client.async_list_external_transactions(account_ids=["a1"])
    assert isinstance(exs[0], models.ExternalTransaction)
    cards = await client.async_list_card_transactions(account_id="a1")
    assert isinstance(cards[0], models.Transaction)
    logs = await client.async_list_audit_logs()
    assert isinstance(logs[0], models.AuditLogEntry)


# Add more tests for balance and account helpers


def test_get_pod_accounts():
    """Test filtering Pod accounts."""
    client = SequenceApiClient(None, "token")
    data = {
        "data": {
            "accounts": [
                {
                    "id": "1",
                    "type": "Pod",
                    "balance": {"amountInDollars": 100, "error": None},
                },
                {
                    "id": "2",
                    "type": "Income Source",
                    "balance": {"amountInDollars": 50, "error": None},
                },
            ]
        }
    }
    pods = client.get_pod_accounts(data)
    assert len(pods) == 1
    assert pods[0]["type"] == "Pod"


def test_get_total_balance():
    """Test total balance calculation across all accounts."""
    client = SequenceApiClient(None, "token")
    data = {
        "data": {
            "accounts": [
                {
                    "id": "1",
                    "type": "Pod",
                    "balance": {"amountInDollars": 100, "error": None},
                },
                {
                    "id": "2",
                    "type": "Income Source",
                    "balance": {"amountInDollars": 50, "error": None},
                },
                {
                    "id": "3",
                    "type": "Pod",
                    "balance": {"amountInDollars": None, "error": "err"},
                },
            ]
        }
    }
    total = client.get_total_balance(data)
    assert total == 150


def test_get_income_source_accounts():
    """Test filtering Income Source accounts."""
    client = SequenceApiClient(None, "token")
    data = {
        "data": {
            "accounts": [
                {
                    "id": "1",
                    "type": "Pod",
                    "balance": {"amountInDollars": 100, "error": None},
                },
                {
                    "id": "2",
                    "type": "Income Source",
                    "balance": {"amountInDollars": 50, "error": None},
                },
            ]
        }
    }
    sources = client.get_income_source_accounts(data)
    assert len(sources) == 1
    assert sources[0]["type"] == "Income Source"


def test_get_pod_balance():
    """Test total balance calculation for Pod accounts."""
    client = SequenceApiClient(None, "token")
    data = {
        "data": {
            "accounts": [
                {
                    "id": "1",
                    "type": "Pod",
                    "balance": {"amountInDollars": 100, "error": None},
                },
                {
                    "id": "2",
                    "type": "Pod",
                    "balance": {"amountInDollars": 50, "error": None},
                },
                {
                    "id": "3",
                    "type": "Pod",
                    "balance": {"amountInDollars": None, "error": "err"},
                },
            ]
        }
    }
    total = client.get_pod_balance(data)
    assert total == 150


def test_get_liability_accounts_type():
    """Test filtering Liability accounts by type."""
    client = SequenceApiClient(None, "token")
    data = {
        "data": {
            "accounts": [
                {
                    "id": "1",
                    "type": "Liability",
                    "balance": {"amountInDollars": 10, "error": None},
                },
                {
                    "id": "2",
                    "type": "Pod",
                    "balance": {"amountInDollars": 20, "error": None},
                },
            ]
        }
    }
    liabilities = client.get_liability_accounts(data)
    assert len(liabilities) == 1
    assert liabilities[0]["type"] == "Liability"


def test_get_liability_accounts_ids():
    """Test filtering Liability accounts by configured IDs."""
    client = SequenceApiClient(None, "token")
    data = {
        "data": {
            "accounts": [
                {
                    "id": "1",
                    "type": "Account",
                    "balance": {"amountInDollars": 10, "error": None},
                },
                {
                    "id": "2",
                    "type": "Pod",
                    "balance": {"amountInDollars": 20, "error": None},
                },
            ]
        }
    }
    liabilities = client.get_liability_accounts(data, ["1"])
    assert len(liabilities) == 1
    assert liabilities[0]["id"] == "1"


def test_get_investment_accounts_type():
    """Test filtering Investment accounts by type."""
    client = SequenceApiClient(None, "token")
    data = {
        "data": {
            "accounts": [
                {
                    "id": "1",
                    "type": "Investment",
                    "balance": {"amountInDollars": 10, "error": None},
                },
                {
                    "id": "2",
                    "type": "Pod",
                    "balance": {"amountInDollars": 20, "error": None},
                },
            ]
        }
    }
    investments = client.get_investment_accounts(data)
    assert len(investments) == 1
    assert investments[0]["type"] == "Investment"


def test_get_investment_accounts_ids():
    """Test filtering Investment accounts by configured IDs."""
    client = SequenceApiClient(None, "token")
    data = {
        "data": {
            "accounts": [
                {
                    "id": "1",
                    "type": "Account",
                    "balance": {"amountInDollars": 10, "error": None},
                },
                {
                    "id": "2",
                    "type": "Pod",
                    "balance": {"amountInDollars": 20, "error": None},
                },
            ]
        }
    }
    investments = client.get_investment_accounts(data, ["1"])
    assert len(investments) == 1
    assert investments[0]["id"] == "1"


def test_get_external_accounts():
    """Test filtering External accounts."""
    client = SequenceApiClient(None, "token")
    data = {
        "data": {
            "accounts": [
                {
                    "id": "1",
                    "type": "Account",
                    "balance": {"amountInDollars": 10, "error": None},
                },
                {
                    "id": "2",
                    "type": "Pod",
                    "balance": {"amountInDollars": 20, "error": None},
                },
                {
                    "id": "3",
                    "type": "Income Source",
                    "balance": {"amountInDollars": 30, "error": None},
                },
                {
                    "id": "4",
                    "type": "Liability",
                    "balance": {"amountInDollars": 40, "error": None},
                },
                {
                    "id": "5",
                    "type": "Investment",
                    "balance": {"amountInDollars": 50, "error": None},
                },
            ]
        }
    }
    externals = client.get_external_accounts(data)
    assert len(externals) == 1
    assert externals[0]["type"] == "Account"


def test_get_balance_by_type():
    """Test total balance for a specific account type."""
    client = SequenceApiClient(None, "token")
    data = {
        "data": {
            "accounts": [
                {
                    "id": "1",
                    "type": "Pod",
                    "balance": {"amountInDollars": 10, "error": None},
                },
                {
                    "id": "2",
                    "type": "Pod",
                    "balance": {"amountInDollars": 20, "error": None},
                },
                {
                    "id": "3",
                    "type": "Income Source",
                    "balance": {"amountInDollars": 30, "error": None},
                },
            ]
        }
    }
    total = client.get_balance_by_type(data, "Pod")
    assert total == 30


def test_get_account_types_summary():
    """Test summary of all account types and their totals."""
    client = SequenceApiClient(None, "token")
    data = {
        "data": {
            "accounts": [
                {
                    "id": "1",
                    "type": "Pod",
                    "name": "Pod1",
                    "balance": {"amountInDollars": 10, "error": None},
                },
                {
                    "id": "2",
                    "type": "Pod",
                    "name": "Pod2",
                    "balance": {"amountInDollars": 20, "error": None},
                },
                {
                    "id": "3",
                    "type": "Income Source",
                    "name": "Inc1",
                    "balance": {"amountInDollars": 30, "error": None},
                },
            ]
        }
    }
    summary = client.get_account_types_summary(data)
    assert summary["Pod"]["count"] == 2
    assert summary["Pod"]["total_balance"] == 30
    assert summary["Income Source"]["count"] == 1
    assert summary["Income Source"]["total_balance"] == 30

