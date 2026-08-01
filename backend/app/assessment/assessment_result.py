from dataclasses import dataclass


@dataclass
class ClassicalSecurityAssessment:
    """
    Represents the present-day classical security
    assessment of a cryptographic usage.
    """

    status: str

    risk: str

    message: str


@dataclass
class QuantumSecurityAssessment:
    """
    Represents the post-quantum security assessment
    of a cryptographic usage.
    """

    status: str

    risk: str

    vulnerable: bool

    message: str


@dataclass
class MigrationAssessment:
    """
    Represents whether cryptographic migration
    is required and its priority.
    """

    required: bool

    priority: str

    recommendation: str


@dataclass
class CryptoAssessmentResult:
    """
    Complete cryptographic assessment result.
    """

    classical_security: ClassicalSecurityAssessment

    quantum_security: QuantumSecurityAssessment

    migration: MigrationAssessment