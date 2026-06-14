from enum import Enum


class AccountType(str, Enum):
    """Sequence account types."""

    POD = "POD"
    INCOME_SOURCE = "INCOME_SOURCE"
    EXTERNAL_ACCOUNT = "EXTERNAL_ACCOUNT"