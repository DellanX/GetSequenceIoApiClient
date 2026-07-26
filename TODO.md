# TODO

## Documentation and spec update policy

Whenever a TODO item is started, updated, or completed, update the matching documentation and specs in the same change. At minimum, keep these aligned:

- `docs/specs/GetSequenceIoApiClient/README.md` (coverage matrix)
- The relevant area spec README (`accounts`, `activity`, `rules`, `audit_logs`)
- Any user-facing docs that describe endpoint support
- For each endpoint spec entry, keep **test conditions** current with:
  - coverage status (`covered`/`missing`)
  - linked pytest test method name(s) as test IDs

## API specs not yet fully implemented

The following OpenAPI endpoints are documented but do not currently have client method support:

| Endpoint | Operation | Implementation status |
|---|---|---|
| `POST /accounts` | `createAccount` | missing |
| `GET /beneficiaries` | `listBeneficiaries` | missing |
| `POST /rules` | `createRule` | missing |
| `PATCH /rules/{id}` | `updateRule` | missing |
| `GET /card-transactions/{id}` | `getCardTransaction` | missing |
| `GET /external-transactions/{id}` | `getExternalTransaction` | missing |

## Test-condition gaps tied to missing endpoint implementations

The following test-condition coverage cannot be completed until endpoint methods exist:

| Endpoint | Missing conditions | Planned test IDs |
|---|---|---|
| `POST /accounts` | create payload serialization; typed create response parsing; error/idempotency handling | `test_async_create_account_serializes_payload`, `test_async_create_account_returns_account_model`, `test_async_create_account_error_handling` |
| `GET /beneficiaries` | pagination/filter behavior; typed beneficiary list parsing | `test_async_list_beneficiaries_filters_and_pagination`, `test_async_list_beneficiaries_returns_models` |
| `POST /rules` | create payload serialization; typed rule response parsing | `test_async_create_rule_serializes_payload`, `test_async_create_rule_returns_rule_model` |
| `PATCH /rules/{id}` | patch payload serialization; typed updated-rule response parsing | `test_async_update_rule_serializes_payload`, `test_async_update_rule_returns_rule_model` |
| `GET /card-transactions/{id}` | fetch-by-id method behavior; typed transaction parsing | `test_async_get_card_transaction_returns_transaction_model` |
| `GET /external-transactions/{id}` | fetch-by-id method behavior; typed external transaction parsing | `test_async_get_external_transaction_returns_external_transaction_model` |