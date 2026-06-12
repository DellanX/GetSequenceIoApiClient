"""Comprehensive model tests to increase coverage."""

from GetSequenceIoApiClient.models import (
    Balance,
    LinkedAccountSummary,
    LinkedAccount,
    AccountSummary,
    Account,
    TransferAccountRef,
    Transfer,
    RuleSummary,
    Rule,
    RuleExecutionSummary,
    RuleExecution,
    ExternalTransaction,
    Transaction,
    AuditLogEntry,
    AccountType,
    ExecutionMode,
    TransactionDirection,
    TransactionStatus,
    RuleExecutionStatus,
)


def test_balance_from_and_to_dict_and_properties():
    data_camel = {
        "balanceInCents": 12345,
        "availableBalanceInCents": 10000,
        "lastStatementBalanceInCents": 12000,
        "lastStatementDate": "2024-01-01",
        "nextPaymentMinimumInCents": 500,
        "nextPaymentDueDate": "2024-02-01",
        "balanceLastUpdatedAt": "2024-01-02",
        "error": None,
        "interestRatePercentage": 1.5,
        "originalLoanAmountInCents": 500000,
    }

    b = Balance.from_dict(data_camel)
    assert b.balance_in_dollars == 123.45
    assert b.available_balance_in_dollars == 100.0
    assert b.last_statement_balance_in_dollars == 120.0
    assert b.next_payment_minimum_in_dollars == 5.0
    assert b.original_loan_amount_in_dollars == 5000.0
    d = b.to_dict()
    assert d["balanceInCents"] == 12345
    assert "amountInDollars" in d

    # snake_case variant
    data_snake = {"balance_in_cents": 200}
    b2 = Balance.from_dict(data_snake)
    assert b2.balance_in_dollars == 2.0


def test_linked_account_summary_and_linked_account_roundtrip():
    ls = {
        "id": "la1",
        "name": "LA",
        "type": "POD",
        "description": "desc",
        "externalAccountType": "DEPOSITORY",
        "beneficiaryName": "bn",
        "institutionName": "inst",
        "canBeSource": True,
        "canBeDestination": False,
        "createdAt": "2024-01-01",
        "updatedAt": "2024-01-02",
        "deletedAt": None,
    }
    s = LinkedAccountSummary.from_dict(ls)
    td = s.to_dict()
    assert td["type"] == "POD"

    la = {
        **ls,
        "routingNumber": "111",
        "bankAccountNumber": "222",
        "balance": {"balanceInCents": 1000},
        "savingsTargetInCents": 3000,
    }
    la_obj = LinkedAccount.from_dict(la)
    assert la_obj.savings_target_in_dollars == 30.0
    out = la_obj.to_dict()
    assert out["balance"]["balanceInCents"] == 1000


def test_account_summary_and_account_roundtrip():
    linked = {"id": "la1", "name": "la", "type": "POD", "canBeSource": True, "canBeDestination": True, "createdAt": "2024-01-01", "updatedAt": "2024-01-02"}
    data = {"id": "a1", "name": "A", "type": "POD", "linkedAccount": linked}
    s = AccountSummary.from_dict(data)
    assert s.linked_account.id == "la1"

    full = {**data, "balance": {"balanceInCents": 2500}, "linkedAccount": {**linked, "balance": {"balanceInCents": 2500}}}
    acc = Account.from_dict(full)
    assert acc.balance.balance_in_dollars == 25.0
    od = acc.to_dict()
    assert od["balance"]["balanceInCents"] == 2500


def test_transfer_account_ref_and_transfer_roundtrip():
    ref = {"id": "r1", "name": "n", "type": "POD", "isDeleted": True}
    r = TransferAccountRef.from_dict(ref)
    assert r.is_deleted is True
    r_d = r.to_dict()
    assert r_d["isDeleted"] is True

    t = {
        "id": "t1",
        "amountInCents": 500,
        "direction": "INTERNAL",
        "origin": "RULE",
        "source": ref,
        "destination": ref,
        "status": "COMPLETE",
        "executionMode": "LIVE",
        "ruleId": "rid",
        "ruleExecutionId": "rex",
        "errorCode": None,
        "createdAt": "2024-01-01",
    }
    transfer = Transfer.from_dict(t)
    assert transfer.amount_in_dollars == 5.0
    td = transfer.to_dict()
    assert td["executionMode"] == "LIVE"


def test_rules_and_executions():
    rs = {"id": "ru1", "name": "R", "status": "ACTIVE", "isSupported": True}
    rsum = RuleSummary.from_dict(rs)
    od = rsum.to_dict()
    assert od["isSupported"] is True

    rule = {"id": "r1", "name": "R", "status": "ACTIVE", "trigger": {"x": 1}, "steps": [{"a": 1}]}
    rfull = Rule.from_dict(rule)
    assert rfull.steps == [{"a": 1}]

    re = {"id": "re1", "ruleId": "r1", "status": "EXECUTED", "executionMode": "SIMULATION", "createdAt": "2024-01-01"}
    summary = RuleExecutionSummary.from_dict(re)
    assert summary.status == RuleExecutionStatus.EXECUTED
    assert summary.execution_mode == ExecutionMode.SIMULATION

    rex = {**re, "triggerDetails": {"t": True}, "stepIndexMatched": 2, "conditionsNotMet": True, "transfersAttempted": 1, "transfersCompleted": 0, "transfersFailed": 0, "transfersPending": 0, "transferIds": ["t1"], "errorMessage": "e"}
    re_full = RuleExecution.from_dict(rex)
    od = re_full.to_dict()
    assert od["transferIds"] == ["t1"]


def test_external_and_transaction_and_auditlog():
    ext = {"id": "x1", "accountId": "a1", "amountInCents": 1200, "direction": "MONEY_IN", "status": "PENDING", "description": "d", "transactionDate": "2024-01-01"}
    e = ExternalTransaction.from_dict(ext)
    assert e.amount_in_dollars == 12.0
    od = e.to_dict()
    assert od["status"] == "PENDING"

    acc_ref = {"id": "a1", "name": "n", "type": "POD"}
    tx = {"id": "t1", "cardId": "c1", "cardType": "DEBIT", "account": acc_ref, "direction": "MONEY_OUT", "subtype": "PURCHASE", "status": "COMPLETE", "amountInCents": 300, "description": "s", "createdAt": "2024-01-01", "completedAt": "2024-01-02"}
    tr = Transaction.from_dict(tx)
    assert tr.amount_in_dollars == 3.0

    a = {"id": "al1", "createdAt": "2024-01-01", "apiKeyId": "k1", "apiKeyName": "k", "path": "/x", "action": "CALL", "requestId": "req1", "outcome": "OK"}
    al = AuditLogEntry.from_dict(a)
    assert al.api_key_id == "k1"
    assert al.to_dict()["path"] == "/x"


def test_balance_none_properties_and_account_savings_none():
    b = Balance.from_dict({})
    # all dollar properties should be None when underlying cents are None
    assert b.amount_in_dollars is None
    assert b.balance_in_dollars is None
    assert b.available_balance_in_dollars is None
    assert b.last_statement_balance_in_dollars is None
    assert b.next_payment_minimum_in_dollars is None
    assert b.original_loan_amount_in_dollars is None

    # LinkedAccount and Account savings target None behavior
    la = LinkedAccount.from_dict({"id": "la", "name": "n", "type": "POD", "createdAt": "2024-01-01", "updatedAt": "2024-01-01"})
    assert la.savings_target_in_dollars is None
    acc = Account.from_dict({"id": "a", "name": "A", "type": "POD", "createdAt": "2024-01-01", "updatedAt": "2024-01-01"})
    assert acc.savings_target_in_dollars is None


def test_rule_to_dict_and_transaction_to_dict_serialization():
    rule = Rule.from_dict({"id": "r1", "name": "r", "status": "ENABLED", "steps": []})
    rd = rule.to_dict()
    assert rd["id"] == "r1"

    acc_ref = {"id": "a1", "name": "n", "type": "POD"}
    tx = {"id": "t1", "cardId": "c1", "cardType": "DEBIT", "account": acc_ref, "direction": "MONEY_OUT", "subtype": "PURCHASE", "status": "COMPLETE", "amountInCents": 300, "description": "s", "createdAt": "2024-01-01", "completedAt": "2024-01-02"}
    tr = Transaction.from_dict(tx)
    td = tr.to_dict()
    assert td["account"]["id"] == "a1"


def test_account_savings_target_returns_value():
    data = {"id": "a1", "name": "A", "type": "POD", "savingsTargetInCents": 4500, "createdAt": "2024-01-01", "updatedAt": "2024-01-01"}
    acc = Account.from_dict(data)
    assert acc.savings_target_in_dollars == 45.0
