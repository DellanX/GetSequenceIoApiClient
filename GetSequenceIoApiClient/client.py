"""API client façade composing per-category service objects."""
from __future__ import annotations

from typing import Optional

import aiohttp

from ._base import BaseClient
from .accounts import AccountsService
from .rules import RulesService
from .activity import ActivityService
from .audit_logs import AuditLogsService
from .config import SequenceClientConfig
from .exceptions import SequenceApiError, SequenceAuthError, SequenceConnectionError

__all__ = [
    "SequenceApiClient",
    "SequenceClientConfig",
    "SequenceApiError",
    "SequenceAuthError",
    "SequenceConnectionError",
]


class SequenceApiClient:
    """Client façade that composes per-category service objects.

    Users instantiate this class only; category services are exposed as
    attributes: `client.accounts`, `client.rules`, `client.activity`,
    and `client.audit_logs`.
    """

    def __init__(
        self,
        session: aiohttp.ClientSession,
        access_token: str,
        *,
        config: Optional[SequenceClientConfig] = None,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> None:
        self._base = BaseClient(
            session,
            access_token,
            config=config,
            base_url=base_url,
            timeout=timeout,
        )
        self.accounts = AccountsService(self._base)
        self.rules = RulesService(self._base)
        self.activity = ActivityService(self._base)
        self.audit_logs = AuditLogsService(self._base)
