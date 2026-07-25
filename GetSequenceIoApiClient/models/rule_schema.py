from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal, Optional, TypeAlias

from pydantic import Field

from ._base import SequenceModel
from .account_type import AccountType


class RuleStatus(str, Enum):
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"


class AccountNode(SequenceModel):
    id: str = ""
    type: Optional[AccountType] = None
    name: Optional[str] = None


class TransferCapPeriod(str, Enum):
    PER_TRANSFER = "PER_TRANSFER"
    PER_WEEK = "PER_WEEK"
    PER_MONTH = "PER_MONTH"
    PER_YEAR = "PER_YEAR"


class TransferCap(SequenceModel):
    period: Optional[TransferCapPeriod] = None
    amount_in_cents: int = Field(default=0, alias="amountInCents")


class RuleConditionFact(str, Enum):
    TRANSFER_AMOUNT = "TRANSFER_AMOUNT"
    BALANCE = "BALANCE"
    DATE = "DATE"


class RuleConditionOperator(str, Enum):
    EQUALS = "EQUALS"
    NOT_EQUALS = "NOT_EQUALS"
    GREATER_THAN = "GREATER_THAN"
    LESS_THAN = "LESS_THAN"
    GREATER_THAN_OR_EQUAL = "GREATER_THAN_OR_EQUAL"
    LESS_THAN_OR_EQUAL = "LESS_THAN_OR_EQUAL"


class RuleConditionValueFact(str, Enum):
    TRANSFER_AMOUNT = "TRANSFER_AMOUNT"
    BALANCE = "BALANCE"
    DATE = "DATE"
    LAST_DAY_OF_MONTH = "LAST_DAY_OF_MONTH"
    NEXT_PAYMENT_MINIMUM_AMOUNT = "NEXT_PAYMENT_MINIMUM_AMOUNT"
    LAST_STATEMENT_BALANCE = "LAST_STATEMENT_BALANCE"


class RuleConditionParams(SequenceModel):
    account_id: Optional[str] = Field(default=None, alias="accountId")


class RuleCondition(SequenceModel):
    fact: Optional[RuleConditionFact] = None
    operator: Optional[RuleConditionOperator] = None
    value: Optional[float] = None
    value_fact: Optional[RuleConditionValueFact] = Field(default=None, alias="valueFact")
    params: Optional[RuleConditionParams] = None


class RuleConditionLeaf(SequenceModel):
    condition: RuleCondition


class RuleConditionAny(SequenceModel):
    any: list["ChainableRuleCondition"]


class RuleConditionAll(SequenceModel):
    all: list["ChainableRuleCondition"]


ChainableRuleCondition: TypeAlias = RuleConditionLeaf | RuleConditionAny | RuleConditionAll


class RuleActionBase(SequenceModel):
    source: Optional[AccountNode] = None
    destination: Optional[AccountNode] = None
    group_index: int = Field(default=0, alias="groupIndex")
    up_to_enabled: bool = Field(default=False, alias="upToEnabled")
    limit: Optional[TransferCap] = None
    ach_description: Optional[str] = Field(default=None, alias="achDescription")
    is_direct_deposit: bool = Field(default=False, alias="isDirectDeposit")


class RuleActionFixedAmount(RuleActionBase):
    type: Literal["FIXED"] = "FIXED"
    amount_in_cents: int = Field(default=0, alias="amountInCents")


class RuleActionPercentage(RuleActionBase):
    type: Literal["PERCENTAGE"] = "PERCENTAGE"
    percentage_value: float = Field(default=0.0, alias="percentageValue")
    percentage_target: Optional[Literal["INCOMING_AMOUNT", "SOURCE_ACCOUNT"]] = Field(
        default=None,
        alias="percentageTarget",
    )


class RuleActionTopUp(RuleActionBase):
    type: Literal["TOP_UP"] = "TOP_UP"
    amount_in_cents: Optional[int] = Field(default=None, alias="amountInCents")
    next_payment_minimum_account: Optional[AccountNode] = Field(
        default=None,
        alias="nextPaymentMinimumAccount",
    )
    current_balance_account: Optional[AccountNode] = Field(default=None, alias="currentBalanceAccount")
    last_statement_balance_account: Optional[AccountNode] = Field(
        default=None,
        alias="lastStatementBalanceAccount",
    )


class RuleActionRoundDown(RuleActionBase):
    type: Literal["ROUND_DOWN"] = "ROUND_DOWN"
    amount_in_cents: int = Field(default=0, alias="amountInCents")


class RuleActionNextPaymentMinimum(RuleActionBase):
    type: Literal["NEXT_PAYMENT_MINIMUM"] = "NEXT_PAYMENT_MINIMUM"


class RuleActionTotalAmountDue(RuleActionBase):
    type: Literal["TOTAL_AMOUNT_DUE"] = "TOTAL_AMOUNT_DUE"


class RuleActionLastStatementBalance(RuleActionBase):
    type: Literal["LAST_STATEMENT_BALANCE"] = "LAST_STATEMENT_BALANCE"


class RuleActionPercentageLiabilityBalance(RuleActionBase):
    type: Literal["PERCENTAGE_LIABILITY_BALANCE"] = "PERCENTAGE_LIABILITY_BALANCE"
    percentage_value: float = Field(default=0.0, alias="percentageValue")


RuleAction: TypeAlias = Annotated[
    RuleActionFixedAmount
    | RuleActionPercentage
    | RuleActionTopUp
    | RuleActionRoundDown
    | RuleActionNextPaymentMinimum
    | RuleActionTotalAmountDue
    | RuleActionLastStatementBalance
    | RuleActionPercentageLiabilityBalance,
    Field(discriminator="type"),
]


class RuleStep(SequenceModel):
    conditions: Optional[ChainableRuleCondition] = None
    actions: list[RuleAction] = Field(default_factory=list)


class TriggerManual(SequenceModel):
    type: Literal["MANUAL"] = "MANUAL"
    account_id: str = Field(default="", alias="accountId")


class TriggerScheduled(SequenceModel):
    type: Literal["SCHEDULED"] = "SCHEDULED"
    schedule_type: Optional[
        Literal["ONE_TIME", "DAILY", "WEEKLY", "BI_WEEKLY", "MONTHLY", "EVERY_OTHER_WEEK"]
    ] = Field(default=None, alias="scheduleType")
    start_date: str = Field(default="", alias="startDate")
    account_id: Optional[str] = Field(default=None, alias="accountId")


class TriggerOnFundsTransferred(SequenceModel):
    type: Literal["ON_FUNDS_TRANSFERRED"] = "ON_FUNDS_TRANSFERRED"
    account_id: str = Field(default="", alias="accountId")


Trigger: TypeAlias = Annotated[
    TriggerManual | TriggerScheduled | TriggerOnFundsTransferred,
    Field(discriminator="type"),
]


class ManualTriggerDetails(SequenceModel):
    type: Literal["MANUAL"] = "MANUAL"
    amount_in_cents: Optional[int] = Field(default=None, alias="amountInCents")


class SequenceApiTriggerDetails(SequenceModel):
    type: Literal["SEQUENCE_API"] = "SEQUENCE_API"
    amount_in_cents: Optional[int] = Field(default=None, alias="amountInCents")


class ScheduledTriggerDetails(SequenceModel):
    type: Literal["SCHEDULED"] = "SCHEDULED"
    scheduled_time: Optional[str] = Field(default=None, alias="scheduledTime")


class OnFundsTransferredTriggerDetails(SequenceModel):
    type: Literal["ON_FUNDS_TRANSFERRED"] = "ON_FUNDS_TRANSFERRED"
    amount_in_cents: Optional[int] = Field(default=None, alias="amountInCents")


class RemoteApiTriggerDetails(SequenceModel):
    type: Literal["REMOTE_API"] = "REMOTE_API"


TriggerDetails: TypeAlias = Annotated[
    ManualTriggerDetails
    | SequenceApiTriggerDetails
    | ScheduledTriggerDetails
    | OnFundsTransferredTriggerDetails
    | RemoteApiTriggerDetails,
    Field(discriminator="type"),
]


RuleConditionAny.model_rebuild()
RuleConditionAll.model_rebuild()
