"""Consolidated tests for `AccountsService` and accounts helpers."""

import pytest

from GetSequenceIoApiClient.client import SequenceApiClient
from GetSequenceIoApiClient.accounts import AccountsService
from GetSequenceIoApiClient.models.account import Account
from tests._dummy_client import DummyResponse, DummySession


@pytest.mark.asyncio
async def test_async_get_accounts_multiple_pages():
    a1 = {"id": "a1", "name": "A1", "type": "POD"}
    a2 = {"id": "a2", "name": "A2", "type": "POD"}
    resp1 = DummyResponse(200, {"items": [a1], "pagination": {"page": 1, "pageSize": 1, "hasNextPage": True}})
    resp2 = DummyResponse(200, {"items": [a2], "pagination": {"page": 2, "pageSize": 1, "hasNextPage": False}})
    session = DummySession([resp1, resp2])
    client = SequenceApiClient(session, "token")
    results = await client.accounts.async_get_accounts()
    assert len(results) == 2


@pytest.mark.asyncio
async def test_async_get_accounts_filters_params():
    resp = DummyResponse(200, {"items": [], "pagination": {"page": 1, "pageSize": 10, "hasNextPage": False}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    await client.accounts.async_get_accounts(type="Pod", state="ACTIVE", page=1, page_size=5)
    params = session.last_request["params"]
    assert params.get("type") == "Pod"
    assert params.get("state") == "ACTIVE"
    assert params.get("page") == 1
    assert params.get("pageSize") == 5


# Additional direct AccountsService tests to hit edge branches
class FakeBase:
    def __init__(self):
        self.base_url = "http://api"
        self.last_request = None

    async def _async_request(self, method, url, params=None):
        self.last_request = {"method": method, "url": url, "params": params}
        # return a dict without 'items' to exercise the missing-items branch
        return {}

    async def _async_get_all_pages(self, url, params):
        # simulate two pages
        return [{"id": "p1"}, {"id": "p2"}]


@pytest.mark.asyncio
async def test_async_get_accounts_with_type_and_state_page_calls_request_and_sets_params():
    base = FakeBase()
    svc = AccountsService(base)
    # call with page to force _async_request branch
    res = await svc.async_get_accounts(type="Pod", state="ACTIVE", page=1)
    # ensure params were passed through
    assert base.last_request is not None
    assert base.last_request["params"]["type"] == "Pod"
    assert base.last_request["params"]["state"] == "ACTIVE"
    assert res == []


@pytest.mark.asyncio
async def test_async_get_accounts_without_page_uses_get_all_pages_and_returns_summaries():
    base = FakeBase()
    svc = AccountsService(base)
    res = await svc.async_get_accounts()
    # from our fake _async_get_all_pages we returned dicts that map to AccountSummary
    assert len(res) == 2


@pytest.mark.asyncio
async def test_async_get_account_returns_account_model():
    class BaseOne(FakeBase):
        async def _async_request(self, method, url, params=None):
            return {"id": "acc1", "name": "A", "type": "POD", "balance": {"balanceInCents": 0}}

    base = BaseOne()
    svc = AccountsService(base)
    acct = await svc.async_get_account("acc1")
    assert isinstance(acct, Account)


@pytest.mark.asyncio
async def test_async_test_connection_returns_false_on_exception():
    class BrokenBase(FakeBase):
        async def _async_request(self, method, url, params=None):
            raise RuntimeError("boom")

    svc = AccountsService(BrokenBase())
    ok = await svc.async_test_connection()
    assert ok is False


@pytest.mark.asyncio
async def test_async_test_connection_returns_true_on_success():
    class GoodBase(FakeBase):
        async def _async_request(self, method, url, params=None):
            # return a minimal paged response
            return {"items": [], "pagination": {"page": 1, "pageSize": 1, "hasNextPage": False}}

    svc = AccountsService(GoodBase())
    ok = await svc.async_test_connection()
    assert ok is True
