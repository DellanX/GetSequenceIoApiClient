# Audit Logs Endpoint Specs

Source of truth: `openapi.json` (`Audit Logs` tag)

## Endpoints

### `GET /audit-logs` (`listAuditLog`)
- **Behavior**: list audit log entries with optional filters (`apiKeyId`, `action`, `from`, `to`) and pagination.
- **Client support**: ✅ `GetSequenceIoApiClient/audit_logs.py::AuditLogsService.async_list_audit_logs`
- **Models**: `AuditLogEntry`
- **Query model**: `AuditLogsListParams`
- **Tests**: `tests/audit_logs/test_client_audit.py`, `tests/audit_logs/test_audit_logs_extra.py`
- **Test conditions**:
  - Returns typed audit log entries -> ✅ `test_external_and_card_and_audit_endpoints`, `test_async_list_audit_logs_params_and_models`
  - Encodes `apiKeyId/action` filters -> ✅ `test_async_list_audit_logs_params_and_models`
  - Encodes date and page params -> ✅ `test_audit_logs_params_and_pagination`
  - Aggregates pagination when page not supplied -> ✅ `test_async_list_audit_logs_pagination_concat`

## Notes for future changes

- Keep query alias compatibility in `_params.py` aligned to OpenAPI names.
- Update `AuditLogEntry` model fields when OpenAPI schema changes.
