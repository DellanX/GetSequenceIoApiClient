from enum import Enum


class TransactionDirection(str, Enum):
    """Transaction directions."""

    MONEY_IN = "MONEY_IN"
    MONEY_OUT = "MONEY_OUT"
    INTERNAL = "INTERNAL"