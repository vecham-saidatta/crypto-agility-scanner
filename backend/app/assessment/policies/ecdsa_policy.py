from app.assessment.assessment_result import (
    ClassicalSecurityAssessment,
    QuantumSecurityAssessment,
    MigrationAssessment,
    CryptoAssessmentResult,
)


class ECDSAPolicy:
    """
    Assesses ECDSA usage for classical security,
    quantum exposure, and migration requirements.
    """

    APPROVED_HASHES = {
        "SHA-224",
        "SHA-256",
        "SHA-384",
        "SHA-512",
    }

    DEPRECATED_HASHES = {
        "MD5",
        "SHA-1",
    }

    def assess(
        self,
        hash_algorithm: str | None,
    ) -> CryptoAssessmentResult:

        classical = self._assess_classical_security(
            hash_algorithm
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
        hash_algorithm: str | None,
    ) -> ClassicalSecurityAssessment:

        if hash_algorithm is None:

            return ClassicalSecurityAssessment(
                status="UNKNOWN",
                risk="MEDIUM",
                message=(
                    "ECDSA hash algorithm could not "
                    "be determined statically."
                ),
            )

        if hash_algorithm in self.DEPRECATED_HASHES:

            return ClassicalSecurityAssessment(
                status="DISALLOWED",
                risk="HIGH",
                message=(
                    f"ECDSA is configured with "
                    f"{hash_algorithm}, which requires "
                    "migration to an approved hash."
                ),
            )

        if hash_algorithm in self.APPROVED_HASHES:

            return ClassicalSecurityAssessment(
                status="ACCEPTABLE",
                risk="LOW",
                message=(
                    f"ECDSA uses {hash_algorithm}."
                ),
            )

        return ClassicalSecurityAssessment(
            status="REVIEW_REQUIRED",
            risk="MEDIUM",
            message=(
                f"ECDSA hash algorithm "
                f"{hash_algorithm} requires review."
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
                "ECDSA is vulnerable to sufficiently "
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
                "Plan migration from ECDSA to an "
                "approved post-quantum digital "
                "signature mechanism."
            ),
        )