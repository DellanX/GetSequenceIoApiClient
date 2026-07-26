# GetSequenceIoApiClient Specs

This spec set is the endpoint-by-endpoint crosswalk between `openapi.json` and this client library.

## Endpoint Coverage Summary (from `openapi.json`)

| Area | Endpoint | OpenAPI opId | Client support |
|---|---|---|---|
| Accounts | `GET /accounts` | `listAccounts` | Implemented (`AccountsService.async_get_accounts`) |
| Accounts | `POST /accounts` | `createAccount` | Not implemented |
| Accounts | `GET /accounts/{id}` | `getAccount` | Implemented (`AccountsService.async_get_account`) |
| Accounts | `GET /accounts/{accountId}/transfers` | `listAccountTransfers` | Implemented (`ActivityService.async_list_transfers_by_account`) |
| Accounts | `GET /beneficiaries` | `listBeneficiaries` | Not implemented |
| Rules | `GET /rules` | `listRules` | Implemented (`RulesService.async_list_rules`) |
| Rules | `POST /rules` | `createRule` | Not implemented |
| Rules | `GET /rules/{id}` | `getRule` | Implemented (`RulesService.async_get_rule`) |
| Rules | `PATCH /rules/{id}` | `updateRule` | Not implemented |
| Rules | `POST /rules/{id}/trigger` | `triggerRule` | Implemented (`RulesService.async_trigger_rule`) |
| Rules | `GET /rules/{ruleId}/executions` | `listRuleExecutions` | Implemented (`RulesService.async_list_rule_executions`) |
| Rules | `GET /rules/{ruleId}/executions/{id}` | `getRuleExecution` | Implemented (`RulesService.async_get_rule_execution`) |
| Transfers | `GET /transfers` | `listTransfers` | Implemented (`ActivityService.async_list_transfers`) |
| Transfers | `POST /transfers` | `createTransfer` | Implemented (`ActivityService.async_create_transfer`) |
| Transfers | `GET /transfers/{id}` | `getTransfer` | Implemented (`ActivityService.async_get_transfer`) |
| Card transactions | `GET /card-transactions` | `listTransactions` | Implemented (`ActivityService.async_list_card_transactions`) |
| Card transactions | `GET /card-transactions/{id}` | `getCardTransaction` | Not implemented |
| External transactions | `GET /external-transactions` | `listExternalTransactions` | Implemented (`ActivityService.async_list_external_transactions`) |
| External transactions | `GET /external-transactions/{id}` | `getExternalTransaction` | Not implemented |
| Audit logs | `GET /audit-logs` | `listAuditLog` | Implemented (`AuditLogsService.async_list_audit_logs`) |

## Shared behavior guaranteed by this codebase

- **Auth header + request envelope handling**: `GetSequenceIoApiClient/_base.py::BaseClient._async_request`
- **Error translation** (`401`, non-2xx -> typed exceptions): `GetSequenceIoApiClient/exceptions.py` + `_base.py`
- **Pagination traversal** (`page`/`pageSize` and `hasNextPage`): `BaseClient._async_get_all_pages`
- **Typed model parsing** (`from_dict`): `GetSequenceIoApiClient/models/*`

## Per-area details

- Accounts: `accounts/README.md`
- Activity (transfers + card + external): `activity/README.md`
- Rules: `rules/README.md`
- Audit logs: `audit_logs/README.md`

Service implementation references in these docs should point to:
- `GetSequenceIoApiClient/<api_group>/service.py`

Each area spec also tracks endpoint-level **test conditions**, with:
- coverage status (`covered` / `missing`),
- mapped pytest test method names used as test IDs.
