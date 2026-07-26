# Accounts Endpoint Specs

Source of truth: `openapi.json` (Accounts tag + beneficiaries path)

## Endpoints

### `GET /accounts` (`listAccounts`)
| Field | Value |
|---|---|
| Behavior | List accounts with optional filters (`type`, `state`) and pagination (`page`, `pageSize`). |
| Client support | Implemented (`GetSequenceIoApiClient/accounts/service.py::AccountsService.async_get_accounts`) |
| Models | `AccountSummary` |
| Query model | `AccountsListParams` |
| Tests | `tests/accounts/service/test_client_behavior.py`, `tests/accounts/service/test_service_behavior.py` |

| Test condition | Status | Test IDs |
|---|---|---|
| Returns a list result on success | covered | `test_async_get_accounts_success` |
| Encodes `type/state/page/pageSize` query params | covered | `test_async_get_accounts_filters_params` |
| Aggregates multiple pages when `page` omitted | covered | `test_async_get_accounts_multiple_pages` |
| Uses single-page branch when `page` provided | covered | `test_async_get_accounts_with_type_and_state_page_calls_request_and_sets_params` |
| Converts auth failure to client auth error | covered | `test_async_get_accounts_auth_error` |
| Converts server failure to API error | covered | `test_async_get_accounts_api_error` |

### `POST /accounts` (`createAccount`)
| Field | Value |
|---|---|
| Behavior | Create account (pod/income source) based on request payload. |
| Client support | Not implemented |

| Test condition | Status | Test IDs |
|---|---|---|
| Endpoint method exists and serializes request body | missing | not available |
| Returns typed created-account response | missing | not available |
| Handles idempotency/error paths per API contract | missing | not available |

### `GET /accounts/{id}` (`getAccount`)
| Field | Value |
|---|---|
| Behavior | Fetch full account details for one account id. |
| Client support | Implemented (`GetSequenceIoApiClient/accounts/service.py::AccountsService.async_get_account`) |
| Models | `Account` |
| Tests | `tests/accounts/service/test_client_behavior.py`, `tests/accounts/service/test_service_behavior.py` |

| Test condition | Status | Test IDs |
|---|---|---|
| Parses account response into `Account` model | covered | `test_async_get_account_and_models` |
| Returns `Account` model from service directly | covered | `test_async_get_account_returns_account_model` |

### `GET /accounts/{accountId}/transfers` (`listAccountTransfers`)
| Field | Value |
|---|---|
| Behavior | List transfers where account participates, with filters and pagination. |
| Client support | Implemented (`GetSequenceIoApiClient/activity/service.py::ActivityService.async_list_transfers_by_account`) |
| Models | `Transfer` |
| Query model | `TransfersByAccountListParams` |
| Tests | `tests/activity/service/test_service_behavior.py` |

| Test condition | Status | Test IDs |
|---|---|---|
| Encodes `accountRole` filter and parses model list | covered | `test_async_list_transfers_by_account_params_and_models` |
| Encodes status/execution mode/page size filters | covered | `test_transfers_by_account_status_execution_and_pagesize` |
| Encodes `from/to/origin/rule_execution_id` filters | covered | `test_transfers_by_account_params_include_dates_and_origin` |
| Supports explicit page branch and auto-pagination branch | covered | `test_list_transfers_by_account_variants` |

### `GET /beneficiaries` (`listBeneficiaries`)
| Field | Value |
|---|---|
| Behavior | List organization beneficiaries. |
| Client support | Not implemented |

| Test condition | Status | Test IDs |
|---|---|---|
| Endpoint method exists and supports pagination filters | missing | not available |
| Parses beneficiary list into typed model(s) | missing | not available |

## Notes for future changes

- If Accounts endpoints are added/changed in OpenAPI, update:
  - `GetSequenceIoApiClient/accounts/service.py`
  - `GetSequenceIoApiClient/_params.py`
  - `GetSequenceIoApiClient/models/*` (as needed)
  - `tests/accounts/*` (and activity tests for account-transfer list behavior)
