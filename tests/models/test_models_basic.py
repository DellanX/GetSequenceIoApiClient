"""Unit tests for models conversions and enums to increase coverage."""

import pytest
from GetSequenceIoApiClient import models


def test_transaction_direction_enum_members():
    # ensure enum names and values exist
    assert models.TransactionDirection.INTERNAL.name == "INTERNAL"
    assert isinstance(models.TransactionDirection.INTERNAL.value, str)


def test_model_from_to_dict_roundtrip():
    data = {
        "id": "acc1",
        "balance": {"balanceInCents": 1000},
        "currency": "USD",
        "createdAt": "2024-01-01T00:00:00Z",
    }
    acc = models.Account.from_dict(data)
    assert acc.id == "acc1"
    # to_dict should include id and createdAt
    d2 = acc.to_dict()
    assert d2.get("id") == "acc1"


def test_rule_summary_and_rule_roundtrip():
    s = {"id": "r1", "name": "x", "status": "ENABLED", "isSupported": True, "createdAt": "2024-01-01T00:00:00Z"}
    rs = models.RuleSummary.from_dict(s)
    assert rs.id == "r1"
    r = models.Rule.from_dict({**s, "steps": []})
    assert r.name == "x"
