"""API client façade composing per-category service objects."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import aiohttp

from ._base import BaseClient
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
