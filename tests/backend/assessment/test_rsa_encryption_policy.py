from app.assessment.policies.rsa_encryption_policy import (
    RSAEncryptionPolicy,
)


def test_rsa_oaep_sha256_is_acceptable():

    result = RSAEncryptionPolicy().assess(
        padding="OAEP",
        hash_algorithm="SHA-256",
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )

    assert (
        result.classical_security.risk
        == "LOW"
    )


def test_rsa_oaep_sha384_is_acceptable():

    result = RSAEncryptionPolicy().assess(
        padding="OAEP",
        hash_algorithm="SHA-384",
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )


def test_rsa_oaep_sha1_is_disallowed():

    result = RSAEncryptionPolicy().assess(
        padding="OAEP",
        hash_algorithm="SHA-1",
    )

    assert (
        result.classical_security.status
        == "DISALLOWED"
    )

    assert (
        result.classical_security.risk
        == "HIGH"
    )


def test_rsa_pkcs1v15_requires_review():

    result = RSAEncryptionPolicy().assess(
        padding="PKCS1v15",
        hash_algorithm=None,
    )

    assert (
        result.classical_security.status
        == "REVIEW_REQUIRED"
    )

    assert (
        result.classical_security.risk
        == "MEDIUM"
    )


def test_rsa_encryption_unknown_padding():

    result = RSAEncryptionPolicy().assess(
        padding=None,
        hash_algorithm="SHA-256",
    )

    assert (
        result.classical_security.status
        == "UNKNOWN"
    )

    assert (
        result.classical_security.risk
        == "MEDIUM"
    )


def test_rsa_oaep_unknown_hash():

    result = RSAEncryptionPolicy().assess(
        padding="OAEP",
        hash_algorithm=None,
    )

    assert (
        result.classical_security.status
        == "UNKNOWN"
    )

    assert (
        result.classical_security.risk
        == "MEDIUM"
    )


def test_rsa_encryption_is_quantum_vulnerable():

    result = RSAEncryptionPolicy().assess(
        padding="OAEP",
        hash_algorithm="SHA-256",
    )

    assert (
        result.quantum_security.status
        == "QUANTUM_VULNERABLE"
    )

    assert (
        result.quantum_security.risk
        == "HIGH"
    )

    assert (
        result.quantum_security.vulnerable
        is True
    )


def test_rsa_encryption_requires_migration():

    result = RSAEncryptionPolicy().assess(
        padding="OAEP",
        hash_algorithm="SHA-256",
    )

    assert result.migration.required is True

    assert (
        result.migration.priority
        == "HIGH"
    )