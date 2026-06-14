from enum import Enum


class ExternalAccountType(str, Enum):
    """Sub-types for external accounts."""

    DEPOSITORY = "DEPOSITORY"
    INVESTMENT = "INVESTMENT"
    LIABILITY = "LIABILITY"