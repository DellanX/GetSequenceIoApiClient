# Test Specs

Mirror area for testing strategy and endpoint coverage notes.

## Required layout

- Mirror source structure from `GetSequenceIoApiClient/`.
- For API service tests, keep files under:
  - `tests/accounts/service/`
  - `tests/activity/service/`
  - `tests/rules/service/`
  - `tests/audit_logs/service/`

## Naming guidance

- Name test files by behavior scope, not by temporary intent.
- Preferred names:
  - `test_client_behavior.py`
  - `test_service_behavior.py`
  - `test_service_params.py`
  - `test_missing_endpoints.py` (for not-yet-implemented endpoints with skip guards)
- Avoid generic names like `*_gaps.py`.
