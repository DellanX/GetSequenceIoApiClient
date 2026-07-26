# Activity Endpoint Specs

Source of truth: `openapi.json` tags `Transfers`, `Card transactions`, and `External transactions`.

## Transfers endpoints

### `GET /transfers` (`listTransfers`)
- **Behavior**: list transfers with filters (`accountIds`, status/date filters, execution metadata) and pagination.
- **Client support**: implemented (`GetSequenceIoApiClient/activity/service.py::ActivityService.async_list_transfers`)
- **Models**: `Transfer`
- **Query model**: `TransfersListParams`
- **Tests**: `tests/activity/service/test_client_behavior.py`, `tests/activity/service/test_service_behavior.py`
- **Test conditions**:
  - Encodes `accountIds` and returns typed transfer list -> covered (`test_list_transfers_and_accountids_encoding`)
  - Supports multi-page aggregation when `page` omitted -> covered (`test_list_transfers_pagination`)
  - Supports explicit page branch -> covered (`test_list_transfers_single_page_param`)
  - Encodes full filter set (`from/to/origin/rule_execution_id`) -> covered (`test_transfers_params_include_from_to_origin_and_rule`)
  - Encodes combined filter params (`direction/status/executionMode`) -> covered (`test_list_transfers_page_param_encodes_params_and_returns_items`)

### `POST /transfers` (`createTransfer`)
- **Behavior**: create transfer using source, destination, amount, optional description/simulation, optional `idempotency-key`.
- **Client support**: implemented (`GetSequenceIoApiClient/activity/service.py::ActivityService.async_create_transfer`)
- **Models**: `Transfer`
- **Payload type**: `CreateTransferRequest` (`_types.py`)
- **Tests**: `tests/activity/service/test_client_behavior.py`, `tests/activity/service/test_service_behavior.py`
- **Test conditions**:
  - Sends create payload and parses typed `Transfer` response -> covered (`test_create_and_get_transfer`)
  - Sets `idempotency-key` header when provided -> covered (`test_get_and_create_transfer_and_idempotency_header`)
  - Raises API error on non-success response -> covered (`test_async_create_transfer_raises_api_error_on_500`)

### `GET /transfers/{id}` (`getTransfer`)
- **Behavior**: fetch transfer by id.
- **Client support**: implemented (`GetSequenceIoApiClient/activity/service.py::ActivityService.async_get_transfer`)
- **Models**: `Transfer`
- **Tests**: `tests/activity/service/test_client_behavior.py`, `tests/activity/service/test_service_behavior.py`
- **Test conditions**:
  - Parses transfer detail by id -> covered (`test_create_and_get_transfer`)
  - Returns typed transfer model -> covered (`test_get_and_create_transfer_and_idempotency_header`)

## Card transaction endpoints

### `GET /card-transactions` (`listTransactions`)
- **Behavior**: list card transactions with account/card/date filters and pagination.
- **Client support**: implemented (`GetSequenceIoApiClient/activity/service.py::ActivityService.async_list_card_transactions`)
- **Models**: `Transaction`
- **Query model**: `CardTransactionsListParams`
- **Tests**: `tests/activity/service/test_service_behavior.py`, `tests/audit_logs/service/test_client_behavior.py`
- **Test conditions**:
  - Returns typed card transaction list -> covered (`test_external_and_card_and_audit_endpoints`)
  - Supports explicit page branch -> covered (`test_async_list_card_transactions_page_param_returns_one`)
  - Encodes `accountId/cardId/from/to` filters -> covered (`test_external_and_card_params_included`)
  - Encodes `pageSize` param -> covered (`test_external_and_card_pagesize_param_included`)

### `GET /card-transactions/{id}` (`getCardTransaction`)
- **Behavior**: fetch one card transaction by id.
- **Client support**: not implemented in current client services
- **Test conditions**:
  - Endpoint method exists for fetch-by-id -> missing (no method yet)
  - Parses typed single `Transaction` response -> missing (no method yet)

## External transaction endpoints

### `GET /external-transactions` (`listExternalTransactions`)
- **Behavior**: list external transactions with account/date/status filters and pagination.
- **Client support**: implemented (`GetSequenceIoApiClient/activity/service.py::ActivityService.async_list_external_transactions`)
- **Models**: `ExternalTransaction`
- **Query model**: `ExternalTransactionsListParams`
- **Tests**: `tests/activity/service/test_service_behavior.py`, `tests/audit_logs/service/test_client_behavior.py`
- **Test conditions**:
  - Returns typed external transaction list -> covered (`test_external_and_card_and_audit_endpoints`)
  - Encodes `accountIds/direction/status/from/to` filters -> covered (`test_external_and_card_params_included`)
  - Encodes `pageSize` param -> covered (`test_external_and_card_pagesize_param_included`)
  - Supports explicit page branch path -> covered (`test_list_external_and_card_transactions_paths`)

### `GET /external-transactions/{id}` (`getExternalTransaction`)
- **Behavior**: fetch one external transaction by id.
- **Client support**: not implemented in current client services
- **Test conditions**:
  - Endpoint method exists for fetch-by-id -> missing (no method yet)
  - Parses typed single `ExternalTransaction` response -> missing (no method yet)

## Notes for future changes

- Activity logic currently centralizes three OpenAPI tags in one service (`ActivityService`).
- Endpoint changes should update:
  - `GetSequenceIoApiClient/activity/service.py`
  - `GetSequenceIoApiClient/_params.py`
  - `GetSequenceIoApiClient/models/*` (when schema changes)
  - `tests/activity/*` and any related integration-style client tests
