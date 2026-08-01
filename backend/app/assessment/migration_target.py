from dataclasses import dataclass

from app.assessment.crypto_purpose import (
    CryptoPurpose,
)


@dataclass(frozen=True)
class MigrationTarget:
    """
    Describes the target cryptographic family
    for a post-quantum migration.
    """

    purpose: CryptoPurpose

    migration_family: str

    candidate_standard: str | None

    candidate_algorithm: str | None