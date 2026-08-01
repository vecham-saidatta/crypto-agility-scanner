from app.assessment.policies.rsa_policy import RSAPolicy


def test_rsa_1024_is_classically_disallowed():

    result = RSAPolicy().assess(
        key_size=1024
    )

    assert (
        result.classical_security.status
        == "DISALLOWED"
    )

    assert (
        result.classical_security.risk
        == "HIGH"
    )


def test_rsa_2048_is_classically_acceptable():

    result = RSAPolicy().assess(
        key_size=2048
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )

    assert (
        result.classical_security.risk
        == "LOW"
    )


def test_rsa_3072_is_classically_acceptable():

    result = RSAPolicy().assess(
        key_size=3072
    )

    assert (
        result.classical_security.status
        == "ACCEPTABLE"
    )


def test_rsa_unknown_key_size():

    result = RSAPolicy().assess(
        key_size=None
    )

    assert (
        result.classical_security.status
        == "UNKNOWN"
    )


def test_rsa_is_quantum_vulnerable():

    result = RSAPolicy().assess(
        key_size=2048
    )

    assert (
        result.quantum_security.vulnerable
        is True
    )

    assert (
        result.quantum_security.status
        == "QUANTUM_VULNERABLE"
    )


def test_rsa_requires_pqc_migration():

    result = RSAPolicy().assess(
        key_size=2048
    )

    assert result.migration.required is True

    assert (
        result.migration.priority
        == "HIGH"
    )