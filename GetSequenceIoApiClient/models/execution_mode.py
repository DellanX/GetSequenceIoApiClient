from enum import Enum


class ExecutionMode(str, Enum):
    """Modes for execution."""

    LIVE = "LIVE"
    SIMULATION = "SIMULATION"