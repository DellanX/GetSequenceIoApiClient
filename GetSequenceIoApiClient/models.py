"""Models representing Sequence API schemas."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, List, Optional, Dict


class AccountType(str, Enum):
    """Sequence account types."""
    POD = "POD"
    INCOME_SOURCE = "INCOME_SOURCE"
    EXTERNAL_ACCOUNT = "EXTERNAL_ACCOUNT"


class ExternalAccountType(str, Enum):
    """Sub-types for external accounts."""
    DEPOSITORY = "DEPOSITORY"
    INVESTMENT = "INVESTMENT"
    LIABILITY = "LIABILITY"


class RuleExecutionStatus(str, Enum):
    """Statuses for rule executions."""
    EXECUTED = "EXECUTED"
    PARTIAL = "PARTIAL"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"


class ExecutionMode(str, Enum):
    """Modes for execution."""
    LIVE = "LIVE"
    SIMULATION = "SIMULATION"


class TransactionDirection(str, Enum):
    """Transaction directions."""
    MONEY_IN = "MONEY_IN"
    MONEY_OUT = "MONEY_OUT"
    INTERNAL = "INTERNAL"


class TransactionStatus(str, Enum):
    """Statuses for transaction."""
    PENDING = "PENDING"
    COMPLETE = "COMPLETE"


@dataclass
class Balance:
    """Current balance information for an account."""
    balance_in_cents: Optional[int]
    available_balance_in_cents: Optional[int]
    last_statement_balance_in_cents: Optional[int]
    last_statement_date: Optional[str]
    next_payment_minimum_in_cents: Optional[int]
    next_payment_due_date: Optional[str]
    balance_last_updated_at: Optional[str]
    error: Optional[str]
    interest_rate_percentage: Optional[float]
    original_loan_amount_in_cents: Optional[int]

    @property
    def amount_in_dollars(self) -> Optional[float]:
        """Convert balance_in_cents to dollars for backward compatibility."""
        return self.balance_in_dollars

    @property
    def balance_in_dollars(self) -> Optional[float]:
        """Current balance in dollars."""
        if self.balance_in_cents is None:
            return None
        return self.balance_in_cents / 100.0

    @property
    def available_balance_in_dollars(self) -> Optional[float]:
        """Available balance in dollars."""
        if self.available_balance_in_cents is None:
            return None
        return self.available_balance_in_cents / 100.0

    @property
    def last_statement_balance_in_dollars(self) -> Optional[float]:
        """Last statement balance in dollars."""
        if self.last_statement_balance_in_cents is None:
            return None
        return self.last_statement_balance_in_cents / 100.0

    @property
    def next_payment_minimum_in_dollars(self) -> Optional[float]:
        """Next payment minimum due in dollars."""
        if self.next_payment_minimum_in_cents is None:
            return None
        return self.next_payment_minimum_in_cents / 100.0

    @property
    def original_loan_amount_in_dollars(self) -> Optional[float]:
        """Original loan amount in dollars."""
        if self.original_loan_amount_in_cents is None:
            return None
        return self.original_loan_amount_in_cents / 100.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Balance:
        """Parse Balance from a dictionary supporting both camelCase and snake_case."""
        return cls(
            balance_in_cents=data.get("balanceInCents") if "balanceInCents" in data else data.get("balance_in_cents"),
            available_balance_in_cents=data.get("availableBalanceInCents") if "availableBalanceInCents" in data else data.get("available_balance_in_cents"),
            last_statement_balance_in_cents=data.get("lastStatementBalanceInCents") if "lastStatementBalanceInCents" in data else data.get("last_statement_balance_in_cents"),
            last_statement_date=data.get("lastStatementDate") if "lastStatementDate" in data else data.get("last_statement_date"),
            next_payment_minimum_in_cents=data.get("nextPaymentMinimumInCents") if "nextPaymentMinimumInCents" in data else data.get("next_payment_minimum_in_cents"),
            next_payment_due_date=data.get("nextPaymentDueDate") if "nextPaymentDueDate" in data else data.get("next_payment_due_date"),
            balance_last_updated_at=data.get("balanceLastUpdatedAt") if "balanceLastUpdatedAt" in data else data.get("balance_last_updated_at"),
            error=data.get("error"),
            interest_rate_percentage=data.get("interestRatePercentage") if "interestRatePercentage" in data else data.get("interest_rate_percentage"),
            original_loan_amount_in_cents=data.get("originalLoanAmountInCents") if "originalLoanAmountInCents" in data else data.get("original_loan_amount_in_cents"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary with original camelCase keys."""
        return {
            "balanceInCents": self.balance_in_cents,
            "availableBalanceInCents": self.available_balance_in_cents,
            "lastStatementBalanceInCents": self.last_statement_balance_in_cents,
            "lastStatementDate": self.last_statement_date,
            "nextPaymentMinimumInCents": self.next_payment_minimum_in_cents,
            "nextPaymentDueDate": self.next_payment_due_date,
            "balanceLastUpdatedAt": self.balance_last_updated_at,
            "error": self.error,
            "interestRatePercentage": self.interest_rate_percentage,
            "originalLoanAmountInCents": self.original_loan_amount_in_cents,
            # Backward compatibility field
            "amountInDollars": self.balance_in_dollars,
        }


@dataclass
class LinkedAccountSummary:
    """Lightweight representation of a linked account."""
    id: str
    name: str
    type: AccountType
    description: Optional[str]
    external_account_type: Optional[str]
    beneficiary_name: Optional[str]
    institution_name: Optional[str]
    can_be_source: bool
    can_be_destination: bool
    created_at: str
    updated_at: str
    deleted_at: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> LinkedAccountSummary:
        """Parse LinkedAccountSummary from a dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            type=AccountType(data["type"]) if isinstance(data.get("type"), str) else data.get("type"),
            description=data.get("description"),
            external_account_type=data.get("externalAccountType") if "externalAccountType" in data else data.get("external_account_type"),
            beneficiary_name=data.get("beneficiaryName") if "beneficiaryName" in data else data.get("beneficiary_name"),
            institution_name=data.get("institutionName") if "institutionName" in data else data.get("institution_name"),
            can_be_source=data.get("canBeSource") if "canBeSource" in data else data.get("can_be_source", False),
            can_be_destination=data.get("canBeDestination") if "canBeDestination" in data else data.get("can_be_destination", False),
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            updated_at=data.get("updatedAt") if "updatedAt" in data else data.get("updated_at", ""),
            deleted_at=data.get("deletedAt") if "deletedAt" in data else data.get("deleted_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary with original camelCase keys."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value if isinstance(self.type, AccountType) else self.type,
            "description": self.description,
            "externalAccountType": self.external_account_type,
            "beneficiaryName": self.beneficiary_name,
            "institutionName": self.institution_name,
            "canBeSource": self.can_be_source,
            "canBeDestination": self.can_be_destination,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "deletedAt": self.deleted_at,
        }


@dataclass
class LinkedAccount(LinkedAccountSummary):
    """Full representation of a linked account."""
    routing_number: Optional[str]
    bank_account_number: Optional[str]
    balance: Optional[Balance]
    savings_target_in_cents: Optional[int]

    @property
    def savings_target_in_dollars(self) -> Optional[float]:
        """Savings goal in dollars."""
        if self.savings_target_in_cents is None:
            return None
        return self.savings_target_in_cents / 100.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> LinkedAccount:
        """Parse LinkedAccount from a dictionary."""
        summary = LinkedAccountSummary.from_dict(data)
        bal_data = data.get("balance")
        balance = Balance.from_dict(bal_data) if isinstance(bal_data, dict) else bal_data
        return cls(
            id=summary.id,
            name=summary.name,
            type=summary.type,
            description=summary.description,
            external_account_type=summary.external_account_type,
            beneficiary_name=summary.beneficiary_name,
            institution_name=summary.institution_name,
            can_be_source=summary.can_be_source,
            can_be_destination=summary.can_be_destination,
            created_at=summary.created_at,
            updated_at=summary.updated_at,
            deleted_at=summary.deleted_at,
            routing_number=data.get("routingNumber") if "routingNumber" in data else data.get("routing_number"),
            bank_account_number=data.get("bankAccountNumber") if "bankAccountNumber" in data else data.get("bank_account_number"),
            balance=balance,
            savings_target_in_cents=data.get("savingsTargetInCents") if "savingsTargetInCents" in data else data.get("savings_target_in_cents"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary with original camelCase keys."""
        d = super().to_dict()
        d.update({
            "routingNumber": self.routing_number,
            "bankAccountNumber": self.bank_account_number,
            "balance": self.balance.to_dict() if self.balance else None,
            "savingsTargetInCents": self.savings_target_in_cents,
        })
        return d


@dataclass
class AccountSummary:
    """Lightweight account representation returned by list endpoints."""
    id: str
    name: str
    type: AccountType
    description: Optional[str]
    external_account_type: Optional[str]
    beneficiary_name: Optional[str]
    institution_name: Optional[str]
    can_be_source: bool
    can_be_destination: bool
    linked_account: Optional[LinkedAccountSummary]
    created_at: str
    updated_at: str
    deleted_at: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AccountSummary:
        """Parse AccountSummary from a dictionary."""
        linked_data = data.get("linkedAccount") if "linkedAccount" in data else data.get("linked_account")
        linked_account = LinkedAccountSummary.from_dict(linked_data) if isinstance(linked_data, dict) else linked_data
        return cls(
            id=data.get("id", ""),
            name=data.get("name", ""),
            type=AccountType(data["type"]) if isinstance(data.get("type"), str) else data.get("type"),
            description=data.get("description"),
            external_account_type=data.get("externalAccountType") if "externalAccountType" in data else data.get("external_account_type"),
            beneficiary_name=data.get("beneficiaryName") if "beneficiaryName" in data else data.get("beneficiary_name"),
            institution_name=data.get("institutionName") if "institutionName" in data else data.get("institution_name"),
            can_be_source=data.get("canBeSource") if "canBeSource" in data else data.get("can_be_source", False),
            can_be_destination=data.get("canBeDestination") if "canBeDestination" in data else data.get("can_be_destination", False),
            linked_account=linked_account,
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            updated_at=data.get("updatedAt") if "updatedAt" in data else data.get("updated_at", ""),
            deleted_at=data.get("deletedAt") if "deletedAt" in data else data.get("deleted_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary with original camelCase keys."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value if isinstance(self.type, AccountType) else self.type,
            "description": self.description,
            "externalAccountType": self.external_account_type,
            "beneficiaryName": self.beneficiary_name,
            "institutionName": self.institution_name,
            "canBeSource": self.can_be_source,
            "canBeDestination": self.can_be_destination,
            "linkedAccount": self.linked_account.to_dict() if self.linked_account else None,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "deletedAt": self.deleted_at,
        }


@dataclass
class Account(AccountSummary):
    """Full account representation including masked account details and current balance."""
    routing_number: Optional[str]
    bank_account_number: Optional[str]
    balance: Optional[Balance]
    savings_target_in_cents: Optional[int]
    linked_account: Optional[LinkedAccount]

    @property
    def savings_target_in_dollars(self) -> Optional[float]:
        """Savings goal in dollars."""
        if self.savings_target_in_cents is None:
            return None
        return self.savings_target_in_cents / 100.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Account:
        """Parse Account from a dictionary."""
        summary = AccountSummary.from_dict(data)
        bal_data = data.get("balance")
        balance = Balance.from_dict(bal_data) if isinstance(bal_data, dict) else bal_data
        
        linked_data = data.get("linkedAccount") if "linkedAccount" in data else data.get("linked_account")
        linked_account = LinkedAccount.from_dict(linked_data) if isinstance(linked_data, dict) else linked_data
        
        return cls(
            id=summary.id,
            name=summary.name,
            type=summary.type,
            description=summary.description,
            external_account_type=summary.external_account_type,
            beneficiary_name=summary.beneficiary_name,
            institution_name=summary.institution_name,
            can_be_source=summary.can_be_source,
            can_be_destination=summary.can_be_destination,
            linked_account=linked_account,
            created_at=summary.created_at,
            updated_at=summary.updated_at,
            deleted_at=summary.deleted_at,
            routing_number=data.get("routingNumber") if "routingNumber" in data else data.get("routing_number"),
            bank_account_number=data.get("bankAccountNumber") if "bankAccountNumber" in data else data.get("bank_account_number"),
            balance=balance,
            savings_target_in_cents=data.get("savingsTargetInCents") if "savingsTargetInCents" in data else data.get("savings_target_in_cents"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary with original camelCase keys."""
        d = super().to_dict()
        d.update({
            "routingNumber": self.routing_number,
            "bankAccountNumber": self.bank_account_number,
            "balance": self.balance.to_dict() if self.balance else None,
            "savingsTargetInCents": self.savings_target_in_cents,
            "linkedAccount": self.linked_account.to_dict() if self.linked_account else None,
        })
        return d


@dataclass
class TransferAccountRef:
    """Reference to an account inside a Transfer."""
    id: Optional[str]
    name: str
    type: str
    is_deleted: Optional[bool]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> TransferAccountRef:
        """Parse TransferAccountRef from a dictionary."""
        return cls(
            id=data.get("id"),
            name=data.get("name", ""),
            type=data.get("type", ""),
            is_deleted=data.get("isDeleted") if "isDeleted" in data else data.get("is_deleted"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "isDeleted": self.is_deleted,
        }


@dataclass
class Transfer:
    """A money movement transfer."""
    id: str
    amount_in_cents: int
    direction: TransactionDirection
    origin: str
    source: Optional[TransferAccountRef]
    destination: Optional[TransferAccountRef]
    status: str
    execution_mode: Optional[ExecutionMode]
    rule_id: Optional[str]
    rule_execution_id: Optional[str]
    error_code: Optional[str]
    created_at: str
    completed_at: Optional[str]

    @property
    def amount_in_dollars(self) -> float:
        """Transfer amount in dollars."""
        return self.amount_in_cents / 100.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Transfer:
        """Parse Transfer from a dictionary."""
        src_data = data.get("source")
        source = TransferAccountRef.from_dict(src_data) if isinstance(src_data, dict) else src_data
        
        dest_data = data.get("destination")
        destination = TransferAccountRef.from_dict(dest_data) if isinstance(dest_data, dict) else dest_data
        
        exec_mode = data.get("executionMode") if "executionMode" in data else data.get("execution_mode")
        
        return cls(
            id=data.get("id", ""),
            amount_in_cents=data.get("amountInCents") if "amountInCents" in data else data.get("amount_in_cents", 0),
            direction=TransactionDirection(data["direction"]) if isinstance(data.get("direction"), str) else data.get("direction"),
            origin=data.get("origin", ""),
            source=source,
            destination=destination,
            status=data.get("status", ""),
            execution_mode=ExecutionMode(exec_mode) if isinstance(exec_mode, str) else exec_mode,
            rule_id=data.get("ruleId") if "ruleId" in data else data.get("rule_id"),
            rule_execution_id=data.get("ruleExecutionId") if "ruleExecutionId" in data else data.get("rule_execution_id"),
            error_code=data.get("errorCode") if "errorCode" in data else data.get("error_code"),
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            completed_at=data.get("completedAt") if "completedAt" in data else data.get("completed_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""
        return {
            "id": self.id,
            "amountInCents": self.amount_in_cents,
            "direction": self.direction.value if isinstance(self.direction, TransactionDirection) else self.direction,
            "origin": self.origin,
            "source": self.source.to_dict() if self.source else None,
            "destination": self.destination.to_dict() if self.destination else None,
            "status": self.status,
            "executionMode": self.execution_mode.value if isinstance(self.execution_mode, ExecutionMode) else self.execution_mode,
            "ruleId": self.rule_id,
            "ruleExecutionId": self.rule_execution_id,
            "errorCode": self.error_code,
            "createdAt": self.created_at,
            "completedAt": self.completed_at,
        }


@dataclass
class RuleSummary:
    """Lightweight rule representation returned by list endpoints."""
    id: str
    name: Optional[str]
    description: Optional[str]
    status: str
    is_supported: bool
    created_at: str
    updated_at: str
    deleted_at: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RuleSummary:
        """Parse RuleSummary from a dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name"),
            description=data.get("description"),
            status=data.get("status", ""),
            is_supported=data.get("isSupported") if "isSupported" in data else data.get("is_supported", False),
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            updated_at=data.get("updatedAt") if "updatedAt" in data else data.get("updated_at", ""),
            deleted_at=data.get("deletedAt") if "deletedAt" in data else data.get("deleted_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "isSupported": self.is_supported,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "deletedAt": self.deleted_at,
        }


@dataclass
class Rule:
    """Full representation of a rule."""
    id: str
    name: Optional[str]
    description: Optional[str]
    status: str
    trigger: Optional[Dict[str, Any]]
    steps: List[Dict[str, Any]]
    created_at: str
    updated_at: str
    deleted_at: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Rule:
        """Parse Rule from a dictionary."""
        return cls(
            id=data.get("id", ""),
            name=data.get("name"),
            description=data.get("description"),
            status=data.get("status", ""),
            trigger=data.get("trigger"),
            steps=data.get("steps", []),
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            updated_at=data.get("updatedAt") if "updatedAt" in data else data.get("updated_at", ""),
            deleted_at=data.get("deletedAt") if "deletedAt" in data else data.get("deleted_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "trigger": self.trigger,
            "steps": self.steps,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "deletedAt": self.deleted_at,
        }


@dataclass
class RuleExecutionSummary:
    """Lightweight rule execution representation."""
    id: str
    rule_id: str
    status: RuleExecutionStatus
    execution_mode: ExecutionMode
    created_at: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RuleExecutionSummary:
        """Parse RuleExecutionSummary from a dictionary."""
        status_raw = data.get("status")
        mode_raw = data.get("executionMode") if "executionMode" in data else data.get("execution_mode")
        return cls(
            id=data.get("id", ""),
            rule_id=data.get("ruleId") if "ruleId" in data else data.get("rule_id", ""),
            status=RuleExecutionStatus(status_raw) if isinstance(status_raw, str) else status_raw,
            execution_mode=ExecutionMode(mode_raw) if isinstance(mode_raw, str) else mode_raw,
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""
        return {
            "id": self.id,
            "ruleId": self.rule_id,
            "status": self.status.value if isinstance(self.status, RuleExecutionStatus) else self.status,
            "executionMode": self.execution_mode.value if isinstance(self.execution_mode, ExecutionMode) else self.execution_mode,
            "createdAt": self.created_at,
        }


@dataclass
class RuleExecution(RuleExecutionSummary):
    """Full rule execution details."""
    trigger_details: Optional[Dict[str, Any]]
    step_index_matched: Optional[int]
    conditions_not_met: bool
    transfers_attempted: int
    transfers_completed: int
    transfers_failed: int
    transfers_pending: int
    transfer_ids: List[str]
    error_message: Optional[str]
    next_attempt_at: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> RuleExecution:
        """Parse RuleExecution from a dictionary."""
        summary = RuleExecutionSummary.from_dict(data)
        return cls(
            id=summary.id,
            rule_id=summary.rule_id,
            status=summary.status,
            execution_mode=summary.execution_mode,
            created_at=summary.created_at,
            trigger_details=data.get("triggerDetails") if "triggerDetails" in data else data.get("trigger_details"),
            step_index_matched=data.get("stepIndexMatched") if "stepIndexMatched" in data else data.get("step_index_matched"),
            conditions_not_met=data.get("conditionsNotMet") if "conditionsNotMet" in data else data.get("conditions_not_met", False),
            transfers_attempted=data.get("transfersAttempted") if "transfersAttempted" in data else data.get("transfers_attempted", 0),
            transfers_completed=data.get("transfersCompleted") if "transfersCompleted" in data else data.get("transfers_completed", 0),
            transfers_failed=data.get("transfersFailed") if "transfersFailed" in data else data.get("transfers_failed", 0),
            transfers_pending=data.get("transfersPending") if "transfersPending" in data else data.get("transfers_pending", 0),
            transfer_ids=data.get("transferIds") if "transferIds" in data else data.get("transfer_ids", []),
            error_message=data.get("errorMessage") if "errorMessage" in data else data.get("error_message"),
            next_attempt_at=data.get("nextAttemptAt") if "nextAttemptAt" in data else data.get("next_attempt_at"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""
        d = super().to_dict()
        d.update({
            "triggerDetails": self.trigger_details,
            "stepIndexMatched": self.step_index_matched,
            "conditionsNotMet": self.conditions_not_met,
            "transfersAttempted": self.transfers_attempted,
            "transfersCompleted": self.transfers_completed,
            "transfersFailed": self.transfers_failed,
            "transfersPending": self.transfers_pending,
            "transferIds": self.transfer_ids,
            "errorMessage": self.error_message,
            "nextAttemptAt": self.next_attempt_at,
        })
        return d


@dataclass
class ExternalTransaction:
    """Transaction from Plaid-connected external accounts."""
    id: str
    account_id: str
    amount_in_cents: int
    direction: TransactionDirection
    status: TransactionStatus
    description: str
    transaction_date: str

    @property
    def amount_in_dollars(self) -> float:
        """Transaction amount in dollars."""
        return self.amount_in_cents / 100.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ExternalTransaction:
        """Parse ExternalTransaction from a dictionary."""
        return cls(
            id=data.get("id", ""),
            account_id=data.get("accountId") if "accountId" in data else data.get("account_id", ""),
            amount_in_cents=data.get("amountInCents") if "amountInCents" in data else data.get("amount_in_cents", 0),
            direction=TransactionDirection(data["direction"]) if isinstance(data.get("direction"), str) else data.get("direction"),
            status=TransactionStatus(data["status"]) if isinstance(data.get("status"), str) else data.get("status"),
            description=data.get("description", ""),
            transaction_date=data.get("transactionDate") if "transactionDate" in data else data.get("transaction_date", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""
        return {
            "id": self.id,
            "accountId": self.account_id,
            "amountInCents": self.amount_in_cents,
            "direction": self.direction.value if isinstance(self.direction, TransactionDirection) else self.direction,
            "status": self.status.value if isinstance(self.status, TransactionStatus) else self.status,
            "description": self.description,
            "transactionDate": self.transaction_date,
        }


@dataclass
class Transaction:
    """A settled card transaction on a Sequence-issued card."""
    id: str
    card_id: str
    card_type: str
    account: TransferAccountRef
    direction: TransactionDirection
    subtype: str
    status: str
    amount_in_cents: int
    description: str
    created_at: str
    completed_at: str

    @property
    def amount_in_dollars(self) -> float:
        """Transaction amount in dollars."""
        return self.amount_in_cents / 100.0

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Transaction:
        """Parse Transaction from a dictionary."""
        acc_data = data.get("account")
        account = TransferAccountRef.from_dict(acc_data) if isinstance(acc_data, dict) else acc_data
        return cls(
            id=data.get("id", ""),
            card_id=data.get("cardId") if "cardId" in data else data.get("card_id", ""),
            card_type=data.get("cardType") if "cardType" in data else data.get("card_type", ""),
            account=account,
            direction=TransactionDirection(data["direction"]) if isinstance(data.get("direction"), str) else data.get("direction"),
            subtype=data.get("subtype", ""),
            status=data.get("status", ""),
            amount_in_cents=data.get("amountInCents") if "amountInCents" in data else data.get("amount_in_cents", 0),
            description=data.get("description", ""),
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            completed_at=data.get("completedAt") if "completedAt" in data else data.get("completed_at", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""
        return {
            "id": self.id,
            "cardId": self.card_id,
            "cardType": self.card_type,
            "account": self.account.to_dict() if self.account else None,
            "direction": self.direction.value if isinstance(self.direction, TransactionDirection) else self.direction,
            "subtype": self.subtype,
            "status": self.status,
            "amountInCents": self.amount_in_cents,
            "description": self.description,
            "createdAt": self.created_at,
            "completedAt": self.completed_at,
        }


@dataclass
class AuditLogEntry:
    """An API key audit log entry."""
    id: str
    created_at: str
    api_key_id: str
    api_key_name: str
    path: str
    action: Optional[str]
    request_id: str
    outcome: str
    error_code: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AuditLogEntry:
        """Parse AuditLogEntry from a dictionary."""
        return cls(
            id=data.get("id", ""),
            created_at=data.get("createdAt") if "createdAt" in data else data.get("created_at", ""),
            api_key_id=data.get("apiKeyId") if "apiKeyId" in data else data.get("api_key_id", ""),
            api_key_name=data.get("apiKeyName") if "apiKeyName" in data else data.get("api_key_name", ""),
            path=data.get("path", ""),
            action=data.get("action"),
            request_id=data.get("requestId") if "requestId" in data else data.get("request_id", ""),
            outcome=data.get("outcome", ""),
            error_code=data.get("errorCode") if "errorCode" in data else data.get("error_code"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert object back to a dictionary."""
        return {
            "id": self.id,
            "createdAt": self.created_at,
            "apiKeyId": self.api_key_id,
            "apiKeyName": self.api_key_name,
            "path": self.path,
            "action": self.action,
            "requestId": self.request_id,
            "outcome": self.outcome,
            "errorCode": self.error_code,
        }
