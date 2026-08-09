from app.assessment.assessment_result import (
    ClassicalSecurityAssessment,
    QuantumSecurityAssessment,
    MigrationAssessment,
    CryptoAssessmentResult,
)


class RSASignaturePolicy:
    """
    Assesses RSA digital-signature usage for
    classical security, quantum exposure,
    and migration requirements.
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

    APPROVED_PADDING = {
        "PSS",
        "PKCS1v15",
    }

    def assess(
        self,
        hash_algorithm: str | None,
        padding: str | None,
    ) -> CryptoAssessmentResult:

        classical = self._assess_classical_security(
            hash_algorithm=hash_algorithm,
            padding=padding,
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
        padding: str | None,
    ) -> ClassicalSecurityAssessment:

        if hash_algorithm is None:

            return ClassicalSecurityAssessment(
                status="UNKNOWN",
                risk="MEDIUM",
                message=(
                    "RSA signature hash algorithm "
                    "could not be determined statically."
                ),
            )

        if hash_algorithm in self.DEPRECATED_HASHES:

            return ClassicalSecurityAssessment(
                status="DISALLOWED",
                risk="HIGH",
                message=(
                    f"RSA signature uses "
                    f"{hash_algorithm}, which requires "
                    "migration to an approved hash."
                ),
            )

        if hash_algorithm not in self.APPROVED_HASHES:

            return ClassicalSecurityAssessment(
                status="REVIEW_REQUIRED",
                risk="MEDIUM",
                message=(
                    f"RSA signature hash algorithm "
                    f"{hash_algorithm} requires review."
                ),
            )

        if padding is None:

            return ClassicalSecurityAssessment(
                status="UNKNOWN",
                risk="MEDIUM",
                message=(
                    "RSA signature padding could not "
                    "be determined statically."
                ),
            )

        if padding not in self.APPROVED_PADDING:

            return ClassicalSecurityAssessment(
                status="REVIEW_REQUIRED",
                risk="MEDIUM",
                message=(
                    f"RSA signature padding "
                    f"{padding} requires review."
                ),
            )

        return ClassicalSecurityAssessment(
            status="ACCEPTABLE",
            risk="LOW",
            message=(
                f"RSA signature uses {padding} "
                f"with {hash_algorithm}."
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
                "RSA digital signatures are vulnerable "
                "to sufficiently capable quantum "
                "computers."
            ),
        )

    def _assess_migration(
        self,
    ) -> MigrationAssessment:

        return MigrationAssessment(
            required=True,
            priority="HIGH",
            recommendation=(
                "Plan migration from RSA digital "
                "signatures to an approved "
                "post-quantum digital signature "
                "mechanism."
            ),
        )