from enum import Enum


class TransactionStatus(str, Enum):
    """Statuses for transaction."""

    PENDING = "PENDING"
    COMPLETE = "COMPLETE"