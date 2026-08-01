from app.assessment.assessment_result import (
    ClassicalSecurityAssessment,
    QuantumSecurityAssessment,
    MigrationAssessment,
    CryptoAssessmentResult,
)


class ECDHPolicy:
    """
    Assesses ECDH usage for classical security,
    quantum exposure, and PQC migration.
    """

    def assess(
        self,
    ) -> CryptoAssessmentResult:

        classical = ClassicalSecurityAssessment(
            status="REVIEW_REQUIRED",
            risk="MEDIUM",
            message=(
                "ECDH usage was detected, but the "
                "associated elliptic curve could not "
                "be determined from this finding."
            ),
        )

        quantum = QuantumSecurityAssessment(
            status="QUANTUM_VULNERABLE",
            risk="HIGH",
            vulnerable=True,
            message=(
                "ECDH is vulnerable to sufficiently "
                "capable quantum computers."
            ),
        )

        migration = MigrationAssessment(
            required=True,
            priority="HIGH",
            recommendation=(
                "Plan migration from ECDH to an "
                "approved post-quantum "
                "key-establishment mechanism."
            ),
        )

        return CryptoAssessmentResult(
            classical_security=classical,
            quantum_security=quantum,
            migration=migration,
        )