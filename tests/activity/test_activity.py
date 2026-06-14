"""Consolidated ActivityService tests."""

import pytest
from GetSequenceIoApiClient.client import SequenceApiClient
from GetSequenceIoApiClient.activity import ActivityService
from GetSequenceIoApiClient.exceptions import SequenceApiError
from GetSequenceIoApiClient.models.external_transaction import ExternalTransaction
from GetSequenceIoApiClient.models.transaction import Transaction
from GetSequenceIoApiClient.models.transfer import Transfer
from tests._dummy_client import DummyResponse, DummySession


TRANSFER_ITEM = {
    "id": "t1",
    "amountInCents": 100,
    "direction": "INTERNAL",
    "origin": "RULE",
    "source": None,
    "destination": None,
    "status": "COMPLETE",
    "executionMode": "LIVE",
    "createdAt": "2024-01-01T00:00:00Z",
}


@pytest.mark.asyncio
async def test_async_list_transfers_by_account_params_and_models():
    item = {"id": "t_by_acc", "amountInCents": 150, "direction": "INTERNAL", "origin": "RULE", "source": None, "destination": None, "status": "COMPLETE", "executionMode": "LIVE", "createdAt": "2024-01-01T00:00:00Z"}
    resp = DummyResponse(200, {"items": [item], "pagination": {"page": 1, "pageSize": 10, "hasNextPage": False}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    results = await client.activity.async_list_transfers_by_account("acc1", account_role="SOURCE")
    # verify request params encoded correctly
    assert session.last_request["params"].get("accountRole") == "SOURCE"
    assert isinstance(results[0], Transfer)


@pytest.mark.asyncio
async def test_async_list_card_transactions_page_param_returns_one():
    card_item = {"id": "c_t1", "cardId": "card1", "cardType": "DEBIT_CARD", "account": {"id": "a1", "name": "n", "type": "POD", "isDeleted": False}, "direction": "MONEY_OUT", "subtype": "PURCHASE", "status": "COMPLETE", "amountInCents": 4250, "description": "Coffee", "createdAt": "2024-01-01T00:00:00Z", "completedAt": "2024-01-01T00:00:00Z"}
    resp = DummyResponse(200, {"items": [card_item], "pagination": {"page": 1, "pageSize": 10, "hasNextPage": False}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    cards = await client.activity.async_list_card_transactions(page=1)
    assert len(cards) == 1


@pytest.mark.asyncio
async def test_async_create_transfer_raises_api_error_on_500():
    resp = DummyResponse(500, {"error": {"message": "boom", "code": "X"}})
    session = DummySession(resp)
    client = SequenceApiClient(session, "token")
    with pytest.raises(SequenceApiError):
        await client.activity.async_create_transfer("s", "d", 1000)


@pytest.mark.asyncio
async def test_list_transfers_page_param_encodes_params_and_returns_items():
    resp = {"items": [TRANSFER_ITEM], "pagination": {"page": 1, "pageSize": 10, "hasNextPage": False}}
    # Use injection for the request function and capture params
    captured = {}

    async def req(method, url, headers=None, params=None, json=None):
        captured['last_request'] = {'method': method, 'url': url, 'headers': headers, 'params': params, 'json': json}
        return resp

    svc = ActivityService(None, request_func=req)

    items = await svc.async_list_transfers(account_ids=["a1", "a2"], direction="INTERNAL", status="COMPLETE", execution_mode="LIVE", origin="RULE", rule_execution_id="r1", page=1, page_size=10)
    assert isinstance(items, list)
    params = captured['last_request']["params"]
    assert params["accountIds"] == ["a1", "a2"]
    assert params["direction"] == "INTERNAL"
    assert params.get("rule_execution_id") == "r1"


@pytest.mark.asyncio
async def test_list_transfers_no_page_uses_get_all_pages_and_returns_transfer_list():
    pages = [{"items": [TRANSFER_ITEM]}, {"items": [{"id": "t2", **{k: v for k, v in TRANSFER_ITEM.items() if k != 'id'}}]}]
    # Inject a get_all_pages function
    async def get_all(url, params):
        items = []
        for p in pages:
            items.extend(p.get('items', []))
        return items

    svc = ActivityService(None, get_all_pages_func=get_all)

    items = await svc.async_list_transfers()
    assert isinstance(items, list)
    assert len(items) == 2
    assert {t.id for t in items} == {"t1", "t2"}


@pytest.mark.asyncio
async def test_get_and_create_transfer_and_idempotency_header():
    created = {**TRANSFER_ITEM, "id": "new"}
    # Inject request_func to capture headers and return created
    captured = {}

    async def req_create(method, url, headers=None, params=None, json=None):
        captured['last_request'] = {'method': method, 'url': url, 'headers': headers, 'params': params, 'json': json}
        return created

    svc = ActivityService(None, request_func=req_create)
    tx = await svc.async_create_transfer("s", "d", 5000, description="desc", simulation=False, idempotency_key="k1")
    headers = captured['last_request']["headers"] or {}
    assert headers.get("idempotency-key") == "k1"
    assert isinstance(tx, Transfer)

    # Test async_get_transfer using injected request_func
    async def req_get(method, url, headers=None, params=None, json=None):
        return created

    svc2 = ActivityService(None, request_func=req_get)
    fetched = await svc2.async_get_transfer("new")
    assert isinstance(fetched, Transfer)
    assert fetched.id == "new"


@pytest.mark.asyncio
async def test_list_external_and_card_transactions_paths():
    ext_item = {"id": "x1", "accountId": "a1", "amountInCents": 4200, "direction": "MONEY_OUT", "status": "COMPLETE", "description": "X", "transactionDate": "2024-01-01"}
    card_item = {"id": "c1", "cardId": "card1", "cardType": "DEBIT_CARD", "account": {"id": "a1", "name": "n", "type": "POD", "isDeleted": False}, "direction": "MONEY_OUT", "subtype": "PURCHASE", "status": "COMPLETE", "amountInCents": 4250, "description": "Coffee", "createdAt": "2024-01-01T00:00:00Z", "completedAt": "2024-01-01T00:00:00Z"}

    async def req_ext(method, url, headers=None, params=None, json=None):
        return {"items": [ext_item], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}

    svc_ext = ActivityService(None, request_func=req_ext)
    exs = await svc_ext.async_list_external_transactions(account_ids=["a1"], page=1)
    assert isinstance(exs[0], ExternalTransaction)

    async def req_card(method, url, headers=None, params=None, json=None):
        return {"items": [card_item], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}

    svc_card = ActivityService(None, request_func=req_card)
    cards = await svc_card.async_list_card_transactions(account_id="a1", page=1)
    assert isinstance(cards[0], Transaction)


@pytest.mark.asyncio
async def test_list_transfers_by_account_variants():
    resp = {"items": [TRANSFER_ITEM], "pagination": {"page":1,"pageSize":10,"hasNextPage":False}}
    captured = {}

    async def req_by_account(method, url, headers=None, params=None, json=None):
        captured['last_request'] = {'method': method, 'url': url, 'headers': headers, 'params': params, 'json': json}
        return resp

    svc = ActivityService(None, request_func=req_by_account)
    items = await svc.async_list_transfers_by_account("acct1", account_role="SENDER", direction="INTERNAL", page=1)
    assert isinstance(items, list)
    assert captured['last_request']["params"]["accountRole"] == "SENDER"

    # no-page variant using get_all_pages injection
    async def get_all(url, params):
        return [TRANSFER_ITEM]

    svc2 = ActivityService(None, get_all_pages_func=get_all)
    items2 = await svc2.async_list_transfers_by_account("acct1")
    assert len(items2) == 1


@pytest.mark.asyncio
async def test_transfers_by_account_status_execution_and_pagesize():
    captured = {}

    async def req(method, url, headers=None, params=None, json=None):
        captured['last'] = params
        return {"items": [TRANSFER_ITEM], "pagination": {"page":1,"pageSize":5,"hasNextPage": False}}

    svc = ActivityService(None, request_func=req)
    items = await svc.async_list_transfers_by_account("acctX", status="PENDING", execution_mode="SIMULATION", page=1, page_size=5)
    assert captured['last']["status"] == "PENDING"
    assert captured['last']["executionMode"] == "SIMULATION"
    assert captured['last']["pageSize"] == 5


@pytest.mark.asyncio
async def test_external_and_card_pagesize_param_included():
    captured_ext = {}
    captured_card = {}

    async def req_ext(method, url, headers=None, params=None, json=None):
        captured_ext['last'] = params
        return {"items": [], "pagination": {"page":1,"pageSize":20,"hasNextPage": False}}

    async def req_card(method, url, headers=None, params=None, json=None):
        captured_card['last'] = params
        return {"items": [], "pagination": {"page":1,"pageSize":20,"hasNextPage": False}}

    svc_ext = ActivityService(None, request_func=req_ext)
    await svc_ext.async_list_external_transactions(account_ids=["a"], page=1, page_size=20)
    assert captured_ext['last']["pageSize"] == 20

    svc_card = ActivityService(None, request_func=req_card)
    await svc_card.async_list_card_transactions(account_id="a", page=1, page_size=20)
    assert captured_card['last']["pageSize"] == 20


@pytest.mark.asyncio
async def test_missing_request_and_get_all_raise_runtime_error():
    svc = ActivityService(None)
    # missing request_func -> calling a page-based request should raise
    with pytest.raises(RuntimeError):
        await svc.async_list_transfers(page=1)
    # missing get_all_pages -> calling no-page should raise
    with pytest.raises(RuntimeError):
        await svc.async_list_transfers()


@pytest.mark.asyncio
async def test_transfers_params_include_from_to_origin_and_rule():
    captured = {}

    async def req(method, url, headers=None, params=None, json=None):
        captured['last'] = params
        return {"items": [], "pagination": {"page":1, "pageSize":10, "hasNextPage": False}}

    svc = ActivityService(None, request_func=req)
    await svc.async_list_transfers(account_ids=["a"], direction="MONEY_IN", status="PENDING", execution_mode="SIMULATION", from_date="2024-01-01", to_date="2024-02-01", origin="RULE", rule_execution_id="r1", page=1)
    params = captured['last']
    assert params["from"] == "2024-01-01"
    assert params["to"] == "2024-02-01"
    assert params["origin"] == "RULE"
    assert params["rule_execution_id"] == "r1"


@pytest.mark.asyncio
async def test_transfers_by_account_params_include_dates_and_origin():
    captured = {}

    async def req(method, url, headers=None, params=None, json=None):
        captured['last'] = params
        return {"items": [], "pagination": {"page":1, "pageSize":10, "hasNextPage": False}}

    svc = ActivityService(None, request_func=req)
    await svc.async_list_transfers_by_account("acct", account_role="DEST", from_date="2024-01-01", to_date="2024-01-31", origin="USER", rule_execution_id="rx", page=1)
    params = captured['last']
    assert params["from"] == "2024-01-01"
    assert params["to"] == "2024-01-31"
    assert params["origin"] == "USER"
    assert params["rule_execution_id"] == "rx"


@pytest.mark.asyncio
async def test_external_and_card_params_included():
    captured_ext = {}
    captured_card = {}

    async def req_ext(method, url, headers=None, params=None, json=None):
        captured_ext['last'] = params
        return {"items": [], "pagination": {"page":1, "pageSize":10, "hasNextPage": False}}

    async def req_card(method, url, headers=None, params=None, json=None):
        captured_card['last'] = params
        return {"items": [], "pagination": {"page":1, "pageSize":10, "hasNextPage": False}}

    svc_ext = ActivityService(None, request_func=req_ext)
    await svc_ext.async_list_external_transactions(account_ids=["a1"], direction="MONEY_OUT", status="COMPLETE", from_date="2024-01-01", to_date="2024-01-02", page=1)
    assert captured_ext['last']['accountIds'] == ["a1"]

    svc_card = ActivityService(None, request_func=req_card)
    await svc_card.async_list_card_transactions(account_id="a1", card_id="card1", from_date="2024-01-01", to_date="2024-01-02", page=1)
    assert captured_card['last']['cardId'] == "card1"
