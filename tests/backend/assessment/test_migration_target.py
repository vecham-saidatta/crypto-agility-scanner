from app.assessment.crypto_purpose import (
    CryptoPurpose,
)

from app.assessment.migration_target import (
    MigrationTarget,
)


def test_signature_migration_target():

    target = MigrationTarget(
        purpose=(
            CryptoPurpose.DIGITAL_SIGNATURE
        ),
        migration_family=(
            "POST_QUANTUM_SIGNATURE"
        ),
        candidate_standard="NIST FIPS 204",
        candidate_algorithm="ML-DSA",
    )

    assert (
        target.purpose
        == CryptoPurpose.DIGITAL_SIGNATURE
    )

    assert (
        target.migration_family
        == "POST_QUANTUM_SIGNATURE"
    )

    assert (
        target.candidate_algorithm
        == "ML-DSA"
    )


def test_key_establishment_migration_target():

    target = MigrationTarget(
        purpose=(
            CryptoPurpose.KEY_ESTABLISHMENT
        ),
        migration_family="POST_QUANTUM_KEM",
        candidate_standard="NIST FIPS 203",
        candidate_algorithm="ML-KEM",
    )

    assert (
        target.purpose
        == CryptoPurpose.KEY_ESTABLISHMENT
    )

    assert (
        target.migration_family
        == "POST_QUANTUM_KEM"
    )

    assert (
        target.candidate_algorithm
        == "ML-KEM"
    )


def test_unknown_migration_target():

    target = MigrationTarget(
        purpose=CryptoPurpose.UNKNOWN,
        migration_family="UNRESOLVED",
        candidate_standard=None,
        candidate_algorithm=None,
    )

    assert (
        target.purpose
        == CryptoPurpose.UNKNOWN
    )

    assert target.candidate_standard is None
    assert target.candidate_algorithm is None