from app.assessment.policies.rsa_signature_policy import (
    RSASignaturePolicy,
)


def test_rsa_pss_sha256_is_acceptable():

    result = RSASignaturePolicy().assess(
        hash_algorithm="SHA-256",
        padding="PSS",
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )

    assert (
        result.classical_security.risk
        == "LOW"
    )


def test_rsa_pkcs1v15_sha384_is_acceptable():

    result = RSASignaturePolicy().assess(
        hash_algorithm="SHA-384",
        padding="PKCS1v15",
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )


def test_rsa_signature_sha1_is_disallowed():

    result = RSASignaturePolicy().assess(
        hash_algorithm="SHA-1",
        padding="PSS",
    )

    assert (
        result.classical_security.status
        == "DISALLOWED"
    )

    assert (
        result.classical_security.risk
        == "HIGH"
    )


def test_rsa_signature_unknown_hash():

    result = RSASignaturePolicy().assess(
        hash_algorithm=None,
        padding="PSS",
    )

    assert (
        result.classical_security.status
        == "UNKNOWN"
    )

    assert (
        result.classical_security.risk
        == "MEDIUM"
    )


def test_rsa_signature_unknown_padding():

    result = RSASignaturePolicy().assess(
        hash_algorithm="SHA-256",
        padding=None,
    )

    assert (
        result.classical_security.status
        == "UNKNOWN"
    )


def test_rsa_signature_is_quantum_vulnerable():

    result = RSASignaturePolicy().assess(
        hash_algorithm="SHA-256",
        padding="PSS",
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


def test_rsa_signature_requires_migration():

    result = RSASignaturePolicy().assess(
        hash_algorithm="SHA-256",
        padding="PSS",
    )

    assert result.migration.required is True

    assert (
        result.migration.priority
        == "HIGH"
    )