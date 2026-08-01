from app.assessment.policies.ecdh_policy import (
    ECDHPolicy,
)


def test_ecdh_requires_classical_review():

    result = ECDHPolicy().assess()

    assert (
        result.classical_security.status
        == "REVIEW_REQUIRED"
    )

    assert (
        result.classical_security.risk
        == "MEDIUM"
    )


def test_ecdh_is_quantum_vulnerable():

    result = ECDHPolicy().assess()

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


def test_ecdh_requires_pqc_migration():

    result = ECDHPolicy().assess()

    assert result.migration.required is True

    assert (
        result.migration.priority
        == "HIGH"
    )


def test_ecdh_recommends_key_establishment_migration():

    result = ECDHPolicy().assess()

    assert (
        "key-establishment"
        in result.migration.recommendation
    )