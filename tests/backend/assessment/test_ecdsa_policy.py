from app.assessment.policies.ecdsa_policy import (
    ECDSAPolicy,
)


def test_ecdsa_sha256_is_acceptable():

    result = ECDSAPolicy().assess(
        hash_algorithm="SHA-256"
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )

    assert (
        result.classical_security.risk
        == "LOW"
    )


def test_ecdsa_sha384_is_acceptable():

    result = ECDSAPolicy().assess(
        hash_algorithm="SHA-384"
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )


def test_ecdsa_sha512_is_acceptable():

    result = ECDSAPolicy().assess(
        hash_algorithm="SHA-512"
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )


def test_ecdsa_sha1_is_disallowed():

    result = ECDSAPolicy().assess(
        hash_algorithm="SHA-1"
    )

    assert (
        result.classical_security.status
        == "DISALLOWED"
    )

    assert (
        result.classical_security.risk
        == "HIGH"
    )


def test_ecdsa_unknown_hash_is_unknown():

    result = ECDSAPolicy().assess(
        hash_algorithm=None
    )

    assert (
        result.classical_security.status
        == "UNKNOWN"
    )

    assert (
        result.classical_security.risk
        == "MEDIUM"
    )


def test_ecdsa_unrecognized_hash_requires_review():

    result = ECDSAPolicy().assess(
        hash_algorithm="CUSTOM-HASH"
    )

    assert (
        result.classical_security.status
        == "REVIEW_REQUIRED"
    )

    assert (
        result.classical_security.risk
        == "MEDIUM"
    )


def test_ecdsa_is_quantum_vulnerable():

    result = ECDSAPolicy().assess(
        hash_algorithm="SHA-256"
    )

    assert (
        result.quantum_security.status
        == "QUANTUM_VULNERABLE"
    )

    assert (
        result.quantum_security.vulnerable
        is True
    )

    assert (
        result.quantum_security.risk
        == "HIGH"
    )


def test_ecdsa_requires_signature_migration():

    result = ECDSAPolicy().assess(
        hash_algorithm="SHA-256"
    )

    assert result.migration.required is True

    assert (
        result.migration.priority
        == "HIGH"
    )