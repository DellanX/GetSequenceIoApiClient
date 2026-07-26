import inspect

import pytest

from GetSequenceIoApiClient import models
from GetSequenceIoApiClient.accounts import AccountsService
from GetSequenceIoApiClient.client import SequenceApiClient, SequenceApiError
from tests._dummy_client import DummyResponse, DummySession


def _require_method(service_cls, method_name: str):
    method = getattr(service_cls, method_name, None)
    if method is None:
        pytest.skip(f"{service_cls.__name__}.{method_name} is not implemented yet")
    return method


def _build_kwargs(method, candidate_values: dict, *, payload_fallback: dict | None = None):
    sig = inspect.signature(method)
    kwargs = {}
    for name, param in sig.parameters.items():
        if name == "self":
            continue
        if name in candidate_values:
            kwargs[name] = candidate_values[name]
            continue
        if payload_fallback is not None and name in {"payload", "body", "request", "data", "account"}:
            kwargs[name] = payload_fallback
            continue
        if param.default is inspect.Signature.empty:
            raise AssertionError(f"Unsupported required parameter '{name}' for {method.__name__}")
    return kwargs


@pytest.mark.asyncio
async def test_async_create_account_serializes_payload():
    method = _require_method(AccountsService, "async_create_account")
    payload = {
        "id": "acc-new",
        "name": "New Pod",
        "type": "POD",
        "balance": {"balanceInCents": 0},
    }
    session = DummySession(DummyResponse(201, payload))
    client = SequenceApiClient(session, "token")

    kwargs = _build_kwargs(
        method,
        {
            "name": "New Pod",
            "type": "POD",
            "account_type": "POD",
            "beneficiary_id": "ben-1",
            "state": "ACTIVE",
        },
        payload_fallback={"name": "New Pod", "type": "POD", "beneficiaryId": "ben-1"},
    )
    await client.accounts.async_create_account(**kwargs)

    req = session.last_request or {}
    assert req.get("method") == "POST"
    assert req.get("url", "").endswith("/accounts")
    body = req.get("json")
    assert body is not None


@pytest.mark.asyncio
async def test_async_create_account_returns_account_model():
    method = _require_method(AccountsService, "async_create_account")
    payload = {
        "id": "acc-new",
        "name": "New Pod",
        "type": "POD",
        "balance": {"balanceInCents": 0},
    }
    session = DummySession(DummyResponse(201, payload))
    client = SequenceApiClient(session, "token")

    kwargs = _build_kwargs(
        method,
        {"name": "New Pod", "type": "POD", "account_type": "POD"},
        payload_fallback={"name": "New Pod", "type": "POD"},
    )
    result = await client.accounts.async_create_account(**kwargs)
    assert isinstance(result, models.Account)


@pytest.mark.asyncio
async def test_async_create_account_error_handling():
    method = _require_method(AccountsService, "async_create_account")
    session = DummySession(DummyResponse(500, {"error": {"code": "X", "message": "boom"}}))
    client = SequenceApiClient(session, "token")

    kwargs = _build_kwargs(
        method,
        {"name": "New Pod", "type": "POD", "account_type": "POD"},
        payload_fallback={"name": "New Pod", "type": "POD"},
    )
    with pytest.raises(SequenceApiError):
        await client.accounts.async_create_account(**kwargs)


@pytest.mark.asyncio
async def test_async_list_beneficiaries_filters_and_pagination():
    method = _require_method(AccountsService, "async_list_beneficiaries")
    response = {"items": [{"id": "b1", "name": "Beneficiary"}], "pagination": {"page": 1, "pageSize": 10, "hasNextPage": False}}
    session = DummySession(DummyResponse(200, response))
    client = SequenceApiClient(session, "token")

    kwargs = _build_kwargs(
        method,
        {"page": 1, "page_size": 10, "status": "ACTIVE", "type": "BUSINESS"},
    )
    await client.accounts.async_list_beneficiaries(**kwargs)

    req = session.last_request or {}
    assert req.get("method") == "GET"
    assert req.get("url", "").endswith("/beneficiaries")
    params = req.get("params") or {}
    if "page" in kwargs:
        assert params.get("page") == kwargs["page"]


@pytest.mark.asyncio
async def test_async_list_beneficiaries_returns_models():
    method = _require_method(AccountsService, "async_list_beneficiaries")
    response = {"items": [{"id": "b1", "name": "Beneficiary"}], "pagination": {"page": 1, "pageSize": 10, "hasNextPage": False}}
    session = DummySession(DummyResponse(200, response))
    client = SequenceApiClient(session, "token")

    kwargs = _build_kwargs(method, {"page": 1, "page_size": 10})
    beneficiaries = await client.accounts.async_list_beneficiaries(**kwargs)
    assert isinstance(beneficiaries, list)
    assert len(beneficiaries) == 1
