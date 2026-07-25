"""Compatibility shim for local-repo imports.

This repository contains the installable package under ``GetSequenceIoApiClient/``.
When running from the repository root, this module re-exports the inner package
and maps common submodules so imports like ``GetSequenceIoApiClient.client`` work.
"""

from __future__ import annotations

import sys
from importlib import import_module

_inner_pkg = import_module(".GetSequenceIoApiClient", __name__)

for _name in getattr(_inner_pkg, "__all__", []):
    globals()[_name] = getattr(_inner_pkg, _name)

for _submodule in (
    "client",
    "models",
    "models._base",
    "models.account",
    "models.account_summary",
    "models.account_type",
    "models.audit_log_entry",
    "models.balance",
    "models.execution_mode",
    "models.external_account_type",
    "models.external_transaction",
    "models.linked_account",
    "models.linked_account_summary",
    "models.rule",
    "models.rule_execution",
    "models.rule_execution_status",
    "models.rule_execution_summary",
    "models.rule_summary",
    "models.transaction",
    "models.transaction_direction",
    "models.transaction_status",
    "models.transfer",
    "models.transfer_account_ref",
    "_base",
    "_params",
    "_resource",
    "accounts",
    "activity",
    "audit_logs",
    "rules",
    "exceptions",
    "config",
):
    sys.modules[f"{__name__}.{_submodule}"] = import_module(
        f".GetSequenceIoApiClient.{_submodule}",
        __name__,
    )

__all__ = list(getattr(_inner_pkg, "__all__", []))
