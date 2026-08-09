from app.assessment.assessment_result import (
    ClassicalSecurityAssessment,
    QuantumSecurityAssessment,
    MigrationAssessment,
    CryptoAssessmentResult,
)


class RSAEncryptionPolicy:
    """
    Assesses RSA encryption/decryption usage for
    classical security, quantum exposure,
    and migration requirements.
    """

    APPROVED_OAEP_HASHES = {
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
        padding: str | None,
        hash_algorithm: str | None,
    ) -> CryptoAssessmentResult:

        classical = self._assess_classical_security(
            padding=padding,
            hash_algorithm=hash_algorithm,
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
        padding: str | None,
        hash_algorithm: str | None,
    ) -> ClassicalSecurityAssessment:

        if padding is None:

            return ClassicalSecurityAssessment(
                status="UNKNOWN",
                risk="MEDIUM",
                message=(
                    "RSA encryption padding could not "
                    "be determined statically."
                ),
            )

        if padding == "PKCS1v15":

            return ClassicalSecurityAssessment(
                status="REVIEW_REQUIRED",
                risk="MEDIUM",
                message=(
                    "RSA encryption uses PKCS1v15 "
                    "padding and should be reviewed "
                    "for migration to OAEP."
                ),
            )

        if padding != "OAEP":

            return ClassicalSecurityAssessment(
                status="REVIEW_REQUIRED",
                risk="MEDIUM",
                message=(
                    f"RSA encryption padding "
                    f"{padding} requires review."
                ),
            )

        # From here, padding is OAEP.

        if hash_algorithm is None:

            return ClassicalSecurityAssessment(
                status="UNKNOWN",
                risk="MEDIUM",
                message=(
                    "RSA OAEP hash algorithm could "
                    "not be determined statically."
                ),
            )

        if hash_algorithm in self.DEPRECATED_HASHES:

            return ClassicalSecurityAssessment(
                status="DISALLOWED",
                risk="HIGH",
                message=(
                    f"RSA OAEP uses "
                    f"{hash_algorithm}, which requires "
                    "migration to an approved hash."
                ),
            )

        if hash_algorithm in self.APPROVED_OAEP_HASHES:

            return ClassicalSecurityAssessment(
                status="ACCEPTABLE",
                risk="LOW",
                message=(
                    f"RSA OAEP uses "
                    f"{hash_algorithm}."
                ),
            )

        return ClassicalSecurityAssessment(
            status="REVIEW_REQUIRED",
            risk="MEDIUM",
            message=(
                f"RSA OAEP hash algorithm "
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
                "RSA encryption is vulnerable to "
                "sufficiently capable quantum "
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
                "Plan migration from RSA encryption "
                "to an approved post-quantum "
                "key-establishment mechanism."
            ),
        )