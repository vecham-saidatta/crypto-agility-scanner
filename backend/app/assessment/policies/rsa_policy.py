from app.assessment.assessment_result import (
    ClassicalSecurityAssessment,
    QuantumSecurityAssessment,
    MigrationAssessment,
    CryptoAssessmentResult,
)


class RSAPolicy:
    """
    Assesses RSA usage for classical security,
    quantum exposure, and migration requirements.
    """

    def assess(
        self,
        key_size: int | None,
    ) -> CryptoAssessmentResult:

        classical = self._assess_classical_security(
            key_size
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
        key_size: int | None,
    ) -> ClassicalSecurityAssessment:

        if key_size is None:
            return ClassicalSecurityAssessment(
                status="UNKNOWN",
                risk="MEDIUM",
                message=(
                    "RSA key size could not be "
                    "determined statically."
                ),
            )

        if key_size < 2048:
            return ClassicalSecurityAssessment(
                status="DISALLOWED",
                risk="HIGH",
                message=(
                    "RSA key size is below the "
                    "2048-bit minimum."
                ),
            )

        return ClassicalSecurityAssessment(
            status="ACCEPTABLE",
            risk="LOW",
            message=(
                "RSA key size meets the current "
                "minimum classical-security threshold."
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
                "RSA is vulnerable to sufficiently "
                "capable quantum computers."
            ),
        )

    def _assess_migration(
        self,
    ) -> MigrationAssessment:

        return MigrationAssessment(
            required=True,
            priority="HIGH",
            recommendation=(
                "Plan migration from RSA to an "
                "approved post-quantum alternative "
                "appropriate to the RSA use case."
            ),
        )