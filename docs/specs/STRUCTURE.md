# Specs Structure Mapping

Current mirrored roots:

- `GetSequenceIoApiClient/`
  - `accounts/`
  - `activity/`
  - `audit_logs/`
  - `rules/`
  - `models/`
- `tests/`
- `scripts/`

As new top-level directories or package modules are added, mirror them under `docs/specs/` to keep specs aligned with code structure.

## Source structure convention

- API groups are packages, not flat modules.
- Canonical pattern:
  - `GetSequenceIoApiClient/<api_group>/service.py`
  - `GetSequenceIoApiClient/<api_group>/__init__.py` exports the service class.

Examples:
- `GetSequenceIoApiClient/accounts/service.py`
- `GetSequenceIoApiClient/activity/service.py`
- `GetSequenceIoApiClient/rules/service.py`
- `GetSequenceIoApiClient/audit_logs/service.py`

## Test structure convention

- `tests/` mirrors `GetSequenceIoApiClient/`.
- If multiple test files cover one source file, place them in a folder named after that source file (without `.py`).
- For services, use:
  - `tests/<api_group>/service/`
- Test filenames should describe scope/feature (for example `test_client_behavior.py`, `test_service_params.py`, `test_missing_endpoints.py`).
- Do not use generic suffix buckets like `*_gaps.py`.
