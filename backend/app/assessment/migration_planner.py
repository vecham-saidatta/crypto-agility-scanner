from app.assessment.crypto_purpose import (
    CryptoPurpose,
)

from app.assessment.migration_target import (
    MigrationTarget,
)

from app.scanners.findings import Finding


class MigrationPlanner:
    """
    Maps detected cryptographic usage to an
    appropriate post-quantum migration target.
    """

    def plan(
        self,
        finding: Finding,
    ) -> MigrationTarget:

        if finding.algorithm == "ECDSA":
            return MigrationTarget(
                purpose=(
                    CryptoPurpose.DIGITAL_SIGNATURE
                ),
                migration_family=(
                    "POST_QUANTUM_SIGNATURE"
                ),
                candidate_standard=(
                    "NIST FIPS 204"
                ),
                candidate_algorithm="ML-DSA",
            )

        if finding.algorithm == "ECDH":
            return MigrationTarget(
                purpose=(
                    CryptoPurpose.KEY_ESTABLISHMENT
                ),
                migration_family=(
                    "POST_QUANTUM_KEM"
                ),
                candidate_standard=(
                    "NIST FIPS 203"
                ),
                candidate_algorithm="ML-KEM",
            )

        return MigrationTarget(
            purpose=CryptoPurpose.UNKNOWN,
            migration_family="UNRESOLVED",
            candidate_standard=None,
            candidate_algorithm=None,
        )