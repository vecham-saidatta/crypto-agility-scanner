from app.assessment.assessment_result import (
    ClassicalSecurityAssessment,
    QuantumSecurityAssessment,
    MigrationAssessment,
    CryptoAssessmentResult,
)


def test_crypto_assessment_result():

    classical = ClassicalSecurityAssessment(
        status="ACCEPTABLE",
        risk="LOW",
        message="Classical security assessment.",
    )

    quantum = QuantumSecurityAssessment(
        status="QUANTUM_VULNERABLE",
        risk="HIGH",
        vulnerable=True,
        message="Algorithm is vulnerable to quantum attacks.",
    )

    migration = MigrationAssessment(
        required=True,
        priority="HIGH",
        recommendation=(
            "Plan migration to post-quantum cryptography."
        ),
    )

    result = CryptoAssessmentResult(
        classical_security=classical,
        quantum_security=quantum,
        migration=migration,
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )

    assert (
        result.quantum_security.vulnerable
        is True
    )

    assert (
        result.migration.required
        is True
    )

    assert (
        result.migration.priority
        == "HIGH"
    )