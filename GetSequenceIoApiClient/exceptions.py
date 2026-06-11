"""Exceptions for the Sequence API client."""

class SequenceApiError(Exception):
    """Base exception for Sequence API errors."""


class SequenceAuthError(SequenceApiError):
    """Authentication error with Sequence API."""


class SequenceConnectionError(SequenceApiError):
    """Connection error with Sequence API."""
