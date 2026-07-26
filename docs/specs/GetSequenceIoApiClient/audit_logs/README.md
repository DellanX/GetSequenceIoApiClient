# Audit Logs Endpoint Specs

Source of truth: `openapi.json` (`Audit Logs` tag)

## Endpoints

### `GET /audit-logs` (`listAuditLog`)
- **Behavior**: list audit log entries with optional filters (`apiKeyId`, `action`, `from`, `to`) and pagination.
- **Client support**: implemented (`GetSequenceIoApiClient/audit_logs/service.py::AuditLogsService.async_list_audit_logs`)
- **Models**: `AuditLogEntry`
- **Query model**: `AuditLogsListParams`
- **Tests**: `tests/audit_logs/service/test_client_behavior.py`, `tests/audit_logs/service/test_service_behavior.py`
- **Test conditions**:
  - Returns typed audit log entries -> covered (`test_external_and_card_and_audit_endpoints`, `test_async_list_audit_logs_params_and_models`)
  - Encodes `apiKeyId/action` filters -> covered (`test_async_list_audit_logs_params_and_models`)
  - Encodes date and page params -> covered (`test_audit_logs_params_and_pagination`)
  - Aggregates pagination when page not supplied -> covered (`test_async_list_audit_logs_pagination_concat`)

## Notes for future changes

- Keep query alias compatibility in `_params.py` aligned to OpenAPI names.
- Update `AuditLogEntry` model fields when OpenAPI schema changes.
