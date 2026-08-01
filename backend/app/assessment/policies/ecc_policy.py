from app.assessment.assessment_result import (
    ClassicalSecurityAssessment,
    QuantumSecurityAssessment,
    MigrationAssessment,
    CryptoAssessmentResult,
)


class ECCPolicy:
    """
    Assesses elliptic-curve cryptography for
    classical security, quantum exposure,
    and migration requirements.
    """

    APPROVED_CURVES = {
        "SECP256R1": 128,
        "SECP384R1": 192,
        "SECP521R1": 256,
    }

    def assess(
        self,
        curve: str | None,
    ) -> CryptoAssessmentResult:

        classical = self._assess_classical_security(
            curve
        )

        quantum = self._assess_quantum_security()

        migration = self._assess_migration()

        return CryptoAssessmentResult(
            classical_security=classical,
            quantum_security=quantum,
            migration=migration,
        )

    def _assess_classical_security(
        self,
        curve: str | None,
    ) -> ClassicalSecurityAssessment:

        if curve is None:
            return ClassicalSecurityAssessment(
                status="UNKNOWN",
                risk="MEDIUM",
                message=(
                    "Elliptic curve could not be "
                    "determined statically."
                ),
            )

        if curve in self.APPROVED_CURVES:

            security_strength = (
                self.APPROVED_CURVES[curve]
            )

            return ClassicalSecurityAssessment(
                status="ACCEPTABLE",
                risk="LOW",
                message=(
                    f"{curve} provides approximately "
                    f"{security_strength}-bit classical "
                    "security strength."
                ),
            )

        return ClassicalSecurityAssessment(
            status="REVIEW_REQUIRED",
            risk="MEDIUM",
            message=(
                f"Curve {curve} requires policy review."
            ),
        )

    def _assess_quantum_security(
        self,
    ) -> QuantumSecurityAssessment:

        return QuantumSecurityAssessment(
            status="QUANTUM_VULNERABLE",
            risk="HIGH",
            vulnerable=True,
            message=(
                "Elliptic-curve cryptography is "
                "vulnerable to sufficiently capable "
                "quantum computers."
            ),
        )

    def _assess_migration(
        self,
    ) -> MigrationAssessment:

        return MigrationAssessment(
            required=True,
            priority="HIGH",
            recommendation=(
                "Plan migration of this elliptic-curve "
                "usage to an appropriate post-quantum "
                "cryptographic mechanism."
            ),
        )