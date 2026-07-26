import pytest

from GetSequenceIoApiClient.rules import RulesService


class FakeBase:
    def __init__(self):
        self.base_url = "http://example"
        self.last = {}

    async def _async_request(self, method, url, params=None, headers=None, json=None):
        self.last = {"method": method, "url": url, "params": params, "headers": headers, "json": json}
        return {"items": [{"id": "r1"}], "pagination": {"page": params.get("page", 1) if params else 1, "pageSize": params.get("pageSize", 10) if params else 10, "hasNextPage": False}}

    async def _async_get_all_pages(self, url, params):
        self.last = {"method": "GET", "url": url, "params": params}
        return [{"id": "r1"}]


@pytest.mark.asyncio
async def test_list_rules_with_source_and_page_params():
    fb = FakeBase()
    svc = RulesService(fb)
    items = await svc.async_list_rules(source_id="src", page=1, page_size=5)
    assert fb.last["params"]["sourceId"] == "src"
    assert fb.last["params"]["pageSize"] == 5


@pytest.mark.asyncio
async def test_list_rule_executions_with_filters_and_page():
    fb = FakeBase()
    svc = RulesService(fb)
    items = await svc.async_list_rule_executions("r1", status="EXECUTED", trigger_type="MANUAL", execution_mode="LIVE", from_date="2024-01-01", to_date="2024-01-02", page=1, page_size=2)
    params = fb.last.get("params")
    assert params["status"] == "EXECUTED"
    assert params["triggerType"] == "MANUAL"
    assert params["executionMode"] == "LIVE"
    assert params["pageSize"] == 2
