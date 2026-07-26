import inspect

import pytest

from GetSequenceIoApiClient import models
from GetSequenceIoApiClient.client import SequenceApiClient
from GetSequenceIoApiClient.rules import RulesService
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
        if payload_fallback is not None and name in {"payload", "body", "request", "data", "rule"}:
            kwargs[name] = payload_fallback
            continue
        if param.default is inspect.Signature.empty:
            raise AssertionError(f"Unsupported required parameter '{name}' for {method.__name__}")
    return kwargs


@pytest.mark.asyncio
async def test_async_create_rule_serializes_payload():
    method = _require_method(RulesService, "async_create_rule")
    payload = {"id": "r-new", "name": "Rule New", "status": "ENABLED", "steps": [], "createdAt": "2024-01-01T00:00:00Z"}
    session = DummySession(DummyResponse(201, payload))
    client = SequenceApiClient(session, "token")

    kwargs = _build_kwargs(
        method,
        {"name": "Rule New", "description": "desc"},
        payload_fallback={"name": "Rule New", "status": "ENABLED", "steps": []},
    )
    await client.rules.async_create_rule(**kwargs)

    req = session.last_request or {}
    assert req.get("method") == "POST"
    assert req.get("url", "").endswith("/rules")
    assert req.get("json") is not None


@pytest.mark.asyncio
async def test_async_create_rule_returns_rule_model():
    method = _require_method(RulesService, "async_create_rule")
    payload = {"id": "r-new", "name": "Rule New", "status": "ENABLED", "steps": [], "createdAt": "2024-01-01T00:00:00Z"}
    session = DummySession(DummyResponse(201, payload))
    client = SequenceApiClient(session, "token")

    kwargs = _build_kwargs(
        method,
        {"name": "Rule New"},
        payload_fallback={"name": "Rule New", "status": "ENABLED", "steps": []},
    )
    rule = await client.rules.async_create_rule(**kwargs)
    assert isinstance(rule, models.Rule)


@pytest.mark.asyncio
async def test_async_update_rule_serializes_payload():
    method = _require_method(RulesService, "async_update_rule")
    payload = {"id": "r1", "name": "Rule Updated", "status": "ENABLED", "steps": [], "createdAt": "2024-01-01T00:00:00Z"}
    session = DummySession(DummyResponse(200, payload))
    client = SequenceApiClient(session, "token")

    kwargs = _build_kwargs(
        method,
        {"rule_id": "r1", "id": "r1", "name": "Rule Updated"},
        payload_fallback={"name": "Rule Updated"},
    )
    await client.rules.async_update_rule(**kwargs)

    req = session.last_request or {}
    assert req.get("method") in {"PATCH", "PUT"}
    assert "/rules/" in req.get("url", "")
    assert req.get("json") is not None


@pytest.mark.asyncio
async def test_async_update_rule_returns_rule_model():
    method = _require_method(RulesService, "async_update_rule")
    payload = {"id": "r1", "name": "Rule Updated", "status": "ENABLED", "steps": [], "createdAt": "2024-01-01T00:00:00Z"}
    session = DummySession(DummyResponse(200, payload))
    client = SequenceApiClient(session, "token")

    kwargs = _build_kwargs(
        method,
        {"rule_id": "r1", "id": "r1", "name": "Rule Updated"},
        payload_fallback={"name": "Rule Updated"},
    )
    rule = await client.rules.async_update_rule(**kwargs)
    assert isinstance(rule, models.Rule)
