"""API client façade composing per-category service objects."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import aiohttp

from ._base import BaseClient
from .exceptions import (
    SequenceApiError,
    SequenceAuthError,
    SequenceConnectionError,
)
from .accounts import AccountsService
from .rules import RulesService
from .activity import ActivityService
from .audit_logs import AuditLogsService


class SequenceApiClient:
    """Client façade that composes per-category service objects.

    Users instantiate this class only; category services are exposed as
    attributes: `client.accounts`, `client.rules`, `client.activity`,
    and `client.audit_logs`.
    """

    def __init__(self, session: aiohttp.ClientSession, access_token: str) -> None:
        self._base = BaseClient(session, access_token)
        self.accounts = AccountsService(self._base)
        self.rules = RulesService(self._base)
        self.activity = ActivityService(self._base)
        self.audit_logs = AuditLogsService(self._base)

    # Async convenience wrappers that mirror older flat client API
    async def async_get_accounts(self, *args, **kwargs):
        return await self.accounts.async_get_accounts(*args, **kwargs)

    async def async_get_account(self, *args, **kwargs):
        return await self.accounts.async_get_account(*args, **kwargs)

    async def async_test_connection(self, *args, **kwargs):
        return await self.accounts.async_test_connection(*args, **kwargs)

    async def async_list_transfers(self, *args, **kwargs):
        return await self.activity.async_list_transfers(*args, **kwargs)

    async def async_list_transfers_by_account(self, *args, **kwargs):
        return await self.activity.async_list_transfers_by_account(*args, **kwargs)

    async def async_get_transfer(self, *args, **kwargs):
        return await self.activity.async_get_transfer(*args, **kwargs)

    async def async_create_transfer(self, *args, **kwargs):
        return await self.activity.async_create_transfer(*args, **kwargs)

    async def async_list_external_transactions(self, *args, **kwargs):
        return await self.activity.async_list_external_transactions(*args, **kwargs)

    async def async_list_card_transactions(self, *args, **kwargs):
        return await self.activity.async_list_card_transactions(*args, **kwargs)

    async def async_list_rules(self, *args, **kwargs):
        return await self.rules.async_list_rules(*args, **kwargs)

    async def async_get_rule(self, *args, **kwargs):
        return await self.rules.async_get_rule(*args, **kwargs)

    async def async_trigger_rule(self, *args, **kwargs):
        return await self.rules.async_trigger_rule(*args, **kwargs)

    async def async_list_rule_executions(self, *args, **kwargs):
        return await self.rules.async_list_rule_executions(*args, **kwargs)

    async def async_get_rule_execution(self, *args, **kwargs):
        return await self.rules.async_get_rule_execution(*args, **kwargs)

    async def async_list_audit_logs(self, *args, **kwargs):
        return await self.audit_logs.async_list_audit_logs(*args, **kwargs)

    # Synchronous helper utilities for account lists and balances
    def get_pod_accounts(self, data: dict):
        accounts = (data or {}).get("data", {}).get("accounts", [])
        return [a for a in accounts if str(a.get("type", "")).lower() == "pod"]

    def get_income_source_accounts(self, data: dict):
        accounts = (data or {}).get("data", {}).get("accounts", [])
        return [a for a in accounts if str(a.get("type", "")).lower() == "income source" ]

    def get_external_accounts(self, data: dict):
        accounts = (data or {}).get("data", {}).get("accounts", [])
        return [a for a in accounts if str(a.get("type", "")).lower() == "account"]

    def get_liability_accounts(self, data: dict, ids: list | None = None):
        accounts = (data or {}).get("data", {}).get("accounts", [])
        if ids:
            return [a for a in accounts if a.get("id") in ids]
        return [a for a in accounts if str(a.get("type", "")).lower() == "liability"]

    def get_investment_accounts(self, data: dict, ids: list | None = None):
        accounts = (data or {}).get("data", {}).get("accounts", [])
        if ids:
            return [a for a in accounts if a.get("id") in ids]
        return [a for a in accounts if str(a.get("type", "")).lower() == "investment"]

    def get_total_balance(self, data: dict):
        accounts = (data or {}).get("data", {}).get("accounts", [])
        total = 0
        for a in accounts:
            bal = a.get("balance", {})
            amt = bal.get("amountInDollars")
            err = bal.get("error")
            if amt is None or err:
                continue
            try:
                total += int(amt)
            except Exception:
                pass
        return total

    def get_pod_balance(self, data: dict):
        pods = self.get_pod_accounts(data)
        return self.get_total_balance({"data": {"accounts": pods}})

    def get_balance_by_type(self, data: dict, t: str):
        accounts = (data or {}).get("data", {}).get("accounts", [])
        total = 0
        for a in accounts:
            if str(a.get("type", "")).lower() != str(t).lower():
                continue
            bal = a.get("balance", {})
            amt = bal.get("amountInDollars")
            err = bal.get("error")
            if amt is None or err:
                continue
            try:
                total += int(amt)
            except Exception:
                pass
        return total

    def get_account_types_summary(self, data: dict):
        accounts = (data or {}).get("data", {}).get("accounts", [])
        summary: dict = {}
        for a in accounts:
            t = a.get("type", "Unknown")
            bal = a.get("balance", {})
            amt = bal.get("amountInDollars")
            err = bal.get("error")
            if t not in summary:
                summary[t] = {"count": 0, "total_balance": 0}
            summary[t]["count"] += 1
            if amt is not None and not err:
                try:
                    summary[t]["total_balance"] += int(amt)
                except Exception:
                    pass
        return summary

