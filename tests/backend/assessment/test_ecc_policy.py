from app.assessment.policies.ecc_policy import (
    ECCPolicy,
)


def test_secp256r1_is_classically_acceptable():

    result = ECCPolicy().assess(
        curve="SECP256R1"
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )

    assert (
        result.classical_security.risk
        == "LOW"
    )


def test_secp384r1_is_classically_acceptable():

    result = ECCPolicy().assess(
        curve="SECP384R1"
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )


def test_secp521r1_is_classically_acceptable():

    result = ECCPolicy().assess(
        curve="SECP521R1"
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )


def test_unknown_curve_requires_review():

    result = ECCPolicy().assess(
        curve="CUSTOM_CURVE"
    )

    assert (
        result.classical_security.status
        == "REVIEW_REQUIRED"
    )

    assert (
        result.classical_security.risk
        == "MEDIUM"
    )


def test_dynamic_curve_is_unknown():

    result = ECCPolicy().assess(
        curve=None
    )

    assert (
        result.classical_security.status
        == "UNKNOWN"
    )

    assert (
        result.classical_security.risk
        == "MEDIUM"
    )


def test_ecc_is_quantum_vulnerable():

    result = ECCPolicy().assess(
        curve="SECP256R1"
    )

    assert (
        result.quantum_security.vulnerable
        is True
    )

    assert (
        result.quantum_security.status
        == "QUANTUM_VULNERABLE"
    )

    assert (
        result.quantum_security.risk
        == "HIGH"
    )


def test_ecc_requires_pqc_migration():

    result = ECCPolicy().assess(
        curve="SECP256R1"
    )

    assert (
        result.migration.required
        is True
    )

    assert (
        result.migration.priority
        == "HIGH"
    )