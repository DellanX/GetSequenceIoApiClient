"""Additional tests targeting ActivityService branches."""
import pytest
from GetSequenceIoApiClient.activity import ActivityService
from GetSequenceIoApiClient.models import Transfer, Transaction, ExternalTransaction


class FakeBase:
    # keep for backwards compatibility in some tests, but new tests will
    # prefer injection via request_func / get_all_pages_func
    def __init__(self, response=None, pages=None):
        self.base_url = "http://api"
        self._response = response
        self._pages = pages
        self.last_request = None
        self.last_get_all_params = None

    async def _async_request(self, method, url, headers=None, params=None, json=None):
        self.last_request = {"method": method, "url": url, "headers": headers, "params": params, "json": json}
        return self._response

    async def _async_get_all_pages(self, url, params):
        self.last_get_all_params = params
        if self._pages is None:
            return []
        items = []
        for p in self._pages:
            items.extend(p.get("items", []))
        return items


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
    assert params["rule_execution_id"] == "r1"


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
