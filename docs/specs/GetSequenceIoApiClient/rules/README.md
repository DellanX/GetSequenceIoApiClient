# Rules Endpoint Specs

Source of truth: `openapi.json` (`Rules` tag)

## Endpoints

### `GET /rules` (`listRules`)
- **Behavior**: list rules with optional `sourceId` filter and pagination.
- **Client support**: implemented (`GetSequenceIoApiClient/rules/service.py::RulesService.async_list_rules`)
- **Models**: `RuleSummary`
- **Query model**: `RulesListParams`
- **Tests**: `tests/rules/service/test_client_behavior.py`, `tests/rules/service/test_service_params.py`
- **Test conditions**:
  - Returns typed rule summary list -> covered (`test_rules_endpoints_and_trigger`, `test_async_list_rules_and_get_rule`)
  - Encodes `sourceId/page/pageSize` filters -> covered (`test_async_list_rules_filters_params`, `test_list_rules_with_source_and_page_params`)

### `POST /rules` (`createRule`)
- **Behavior**: create a rule using request body schema.
- **Client support**: not implemented in current client services
- **Test conditions**:
  - Endpoint method exists and serializes create payload -> missing (no method yet)
  - Parses typed created `Rule` response -> missing (no method yet)

### `GET /rules/{id}` (`getRule`)
- **Behavior**: fetch one rule with full steps/conditions/actions.
- **Client support**: implemented (`GetSequenceIoApiClient/rules/service.py::RulesService.async_get_rule`)
- **Models**: `Rule`
- **Tests**: `tests/rules/service/test_client_behavior.py`, `tests/rules/service/test_service_behavior.py`
- **Test conditions**:
  - Parses rule detail response into `Rule` model -> covered (`test_rules_endpoints_and_trigger`, `test_async_list_rules_and_get_rule`)

### `PATCH /rules/{id}` (`updateRule`)
- **Behavior**: update an existing rule.
- **Client support**: not implemented in current client services
- **Test conditions**:
  - Endpoint method exists and serializes patch payload -> missing (no method yet)
  - Parses typed updated `Rule` response -> missing (no method yet)

### `POST /rules/{id}/trigger` (`triggerRule`)
- **Behavior**: enqueue rule execution; accepts simulation/execute amount; optional `idempotency-key`.
- **Client support**: implemented (`GetSequenceIoApiClient/rules/service.py::RulesService.async_trigger_rule`)
- **Response handling**: returns `executionId` string from API response payload.
- **Payload type**: `TriggerRuleRequest` (`_types.py`)
- **Tests**: `tests/rules/service/test_client_behavior.py`, `tests/rules/service/test_service_behavior.py`
- **Test conditions**:
  - Sends trigger payload and returns `executionId` -> covered (`test_rules_endpoints_and_trigger`, `test_async_trigger_rule_returns_execution_id`)
  - Sets `idempotency-key` header when provided -> covered (`test_async_trigger_rule_returns_execution_id`)

### `GET /rules/{ruleId}/executions` (`listRuleExecutions`)
- **Behavior**: list rule executions with status/trigger/date filters and pagination.
- **Client support**: implemented (`GetSequenceIoApiClient/rules/service.py::RulesService.async_list_rule_executions`)
- **Models**: `RuleExecutionSummary`
- **Query model**: `RuleExecutionListParams`
- **Tests**: `tests/rules/service/test_client_behavior.py`, `tests/rules/service/test_service_params.py`, `tests/rules/service/test_service_behavior.py`
- **Test conditions**:
  - Returns typed execution summary list -> covered (`test_rule_executions_get`, `test_async_list_rule_executions_pagination_and_get`)
  - Encodes filters (`status/triggerType/executionMode/from/to/pageSize`) -> covered (`test_list_rule_executions_with_filters_and_page`)
  - Supports pagination flow -> covered (`test_async_list_rule_executions_pagination_and_get`)

### `GET /rules/{ruleId}/executions/{id}` (`getRuleExecution`)
- **Behavior**: fetch one rule execution by execution id.
- **Client support**: implemented (`GetSequenceIoApiClient/rules/service.py::RulesService.async_get_rule_execution`)
- **Models**: `RuleExecution`
- **Tests**: `tests/rules/service/test_client_behavior.py`, `tests/rules/service/test_service_behavior.py`
- **Test conditions**:
  - Parses execution detail into `RuleExecution` model -> covered (`test_rule_executions_get`, `test_async_list_rule_executions_pagination_and_get`)

## Notes for future changes

- Rule schema classes are typed under `GetSequenceIoApiClient/models/rule_schema.py`.
- Any rules contract change should keep request/response type alignment between:
  - service methods (`rules/service.py`),
  - payload types (`_types.py`),
  - models (`models/rule*.py`),
  - tests (`tests/rules/*`).
