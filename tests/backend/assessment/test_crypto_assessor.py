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

def test_assessor_routes_ecc_to_ecc_policy():

    finding = Finding(
        algorithm="ECC",
        file_path="example.py",
        line_number=20,
        severity="INFO",
        status="QUANTUM_VULNERABLE",
        message=(
            "Elliptic-curve key generation detected."
        ),
        recommendation=(
            "PQC migration planning required."
        ),
        reference="",
        metadata={
            "curve": "SECP256R1",
        },
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

def test_assessor_handles_unknown_ecc_curve():

    finding = Finding(
        algorithm="ECC",
        file_path="example.py",
        line_number=20,
        severity="INFO",
        status="QUANTUM_VULNERABLE",
        message=(
            "Elliptic-curve key generation detected."
        ),
        recommendation=(
            "PQC migration planning required."
        ),
        reference="",
        metadata={
            "curve": None,
        },
    )

    result = CryptoAssessor().assess(
        finding
    )

    assert result is not None

    assert (
        result.classical_security.status
        == "UNKNOWN"
    )

def test_assessor_routes_ecdsa_to_ecdsa_policy():

    finding = Finding(
        algorithm="ECDSA",
        file_path="example.py",
        line_number=30,
        severity="INFO",
        status="QUANTUM_VULNERABLE",
        message="ECDSA signature usage detected.",
        recommendation=(
            "PQC signature migration required."
        ),
        reference="NIST FIPS 186-5",
        metadata={
            "hash_algorithm": "SHA-256",
        },
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

def test_assessor_handles_dynamic_ecdsa_hash():

    finding = Finding(
        algorithm="ECDSA",
        file_path="example.py",
        line_number=30,
        severity="INFO",
        status="QUANTUM_VULNERABLE",
        message="ECDSA signature usage detected.",
        recommendation=(
            "PQC signature migration required."
        ),
        reference="NIST FIPS 186-5",
        metadata={
            "hash_algorithm": None,
        },
    )

    result = CryptoAssessor().assess(
        finding
    )

    assert result is not None

    assert (
        result.classical_security.status
        == "UNKNOWN"
    )

    assert (
        result.quantum_security.vulnerable
        is True
    )

def test_assessor_routes_ecdh_to_ecdh_policy():

    finding = Finding(
        algorithm="ECDH",
        file_path="example.py",
        line_number=40,
        severity="INFO",
        status="QUANTUM_VULNERABLE",
        message=(
            "ECDH key-agreement usage detected."
        ),
        recommendation=(
            "Inventory this ECDH usage for "
            "post-quantum key-establishment "
            "migration planning."
        ),
        reference="NIST SP 800-56A Rev. 3",
        metadata={
            "operation": "key_agreement",
        },
    )

    result = CryptoAssessor().assess(
        finding
    )

    assert result is not None

    assert (
        result.classical_security.status
        == "REVIEW_REQUIRED"
    )

    assert (
        result.quantum_security.status
        == "QUANTUM_VULNERABLE"
    )

    assert (
        result.quantum_security.vulnerable
        is True
    )

    assert result.migration.required is True

    assert (
        result.migration.priority
        == "HIGH"
    )