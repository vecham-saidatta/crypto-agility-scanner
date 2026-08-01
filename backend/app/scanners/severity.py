from enum import Enum


class Severity(str, Enum):
    """
    Supported severity levels for findings.
    """

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"