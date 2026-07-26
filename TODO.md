# TODO

## Documentation and spec update policy

Whenever a TODO item is started, updated, or completed, update the matching documentation and specs in the same change. At minimum, keep these aligned:

- `docs/specs/GetSequenceIoApiClient/README.md` (coverage matrix)
- The relevant area spec README (`accounts`, `activity`, `rules`, `audit_logs`)
- Any user-facing docs that describe endpoint support
- For each endpoint spec entry, keep **test conditions** current with:
  - coverage status (`✅`/`❌`)
  - linked pytest test method name(s) as test IDs

## API specs not yet fully implemented

The following OpenAPI endpoints are documented but do not currently have client method support:

1. `POST /accounts` (`createAccount`)
2. `GET /beneficiaries` (`listBeneficiaries`)
3. `POST /rules` (`createRule`)
4. `PATCH /rules/{id}` (`updateRule`)
5. `GET /card-transactions/{id}` (`getCardTransaction`)
6. `GET /external-transactions/{id}` (`getExternalTransaction`)

## Test-condition gaps tied to missing endpoint implementations

The following test-condition coverage cannot be completed until endpoint methods exist:

1. `POST /accounts`
   - Missing conditions: create payload serialization, typed create response parsing, error/idempotency handling.
   - Planned test IDs: `test_async_create_account_serializes_payload`, `test_async_create_account_returns_account_model`, `test_async_create_account_error_handling`.

2. `GET /beneficiaries`
   - Missing conditions: pagination/filter behavior and typed beneficiary list parsing.
   - Planned test IDs: `test_async_list_beneficiaries_filters_and_pagination`, `test_async_list_beneficiaries_returns_models`.

3. `POST /rules`
   - Missing conditions: create payload serialization, typed rule response parsing.
   - Planned test IDs: `test_async_create_rule_serializes_payload`, `test_async_create_rule_returns_rule_model`.

4. `PATCH /rules/{id}`
   - Missing conditions: patch payload serialization, typed updated-rule response parsing.
   - Planned test IDs: `test_async_update_rule_serializes_payload`, `test_async_update_rule_returns_rule_model`.

5. `GET /card-transactions/{id}`
   - Missing conditions: fetch-by-id method behavior and typed transaction parsing.
   - Planned test IDs: `test_async_get_card_transaction_returns_transaction_model`.

6. `GET /external-transactions/{id}`
   - Missing conditions: fetch-by-id method behavior and typed external transaction parsing.
   - Planned test IDs: `test_async_get_external_transaction_returns_external_transaction_model`.