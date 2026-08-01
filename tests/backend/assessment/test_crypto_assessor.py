from app.assessment.crypto_assessor import (
    CryptoAssessor,
)
from app.scanners.findings import Finding


def create_rsa_finding(
    key_size: int | None,
) -> Finding:

    return Finding(
        algorithm="RSA",
        file_path="example.py",
        line_number=10,
        severity="INFO",
        status="QUANTUM_VULNERABLE",
        message="RSA key generation detected.",
        recommendation="Migration planning required.",
        reference="",
        metadata={
            "key_size": key_size,
            "public_exponent": 65537,
        },
    )


def test_assessor_routes_rsa_to_rsa_policy():

    finding = create_rsa_finding(
        key_size=2048
    )

    result = CryptoAssessor().assess(
        finding
    )

    assert result is not None

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )

    assert (
        result.quantum_security.vulnerable
        is True
    )

    assert (
        result.migration.required
        is True
    )


def test_assessor_handles_weak_rsa():

    finding = create_rsa_finding(
        key_size=1024
    )

    result = CryptoAssessor().assess(
        finding
    )

    assert result is not None

    assert (
        result.classical_security.status
        == "DISALLOWED"
    )

    assert (
        result.classical_security.risk
        == "HIGH"
    )


def test_assessor_handles_unknown_rsa_key_size():

    finding = create_rsa_finding(
        key_size=None
    )

    result = CryptoAssessor().assess(
        finding
    )

    assert result is not None

    assert (
        result.classical_security.status
        == "UNKNOWN"
    )


def test_assessor_ignores_unsupported_algorithm():

    finding = Finding(
        algorithm="UNKNOWN",
        file_path="example.py",
        line_number=1,
        severity="INFO",
        status="UNKNOWN",
        message="Test.",
        recommendation="",
        reference="",
        metadata={},
    )

    result = CryptoAssessor().assess(
        finding
    )

    assert result is None