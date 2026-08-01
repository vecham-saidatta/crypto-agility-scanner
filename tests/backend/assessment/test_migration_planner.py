from app.assessment.crypto_purpose import (
    CryptoPurpose,
)

from app.assessment.migration_planner import (
    MigrationPlanner,
)

from app.scanners.findings import Finding

def make_finding(
    algorithm: str,
) -> Finding:

    return Finding(
        algorithm=algorithm,
        file_path="example.py",
        line_number=10,
        severity="INFO",
        status="QUANTUM_VULNERABLE",
        message="Test finding.",
        recommendation="Test recommendation.",
        reference="",
        metadata={},
    )

def test_ecdsa_maps_to_ml_dsa():

    finding = make_finding("ECDSA")

    target = MigrationPlanner().plan(
        finding
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

    assert (
        target.candidate_standard
        == "NIST FIPS 204"
    )

def test_ecdh_maps_to_ml_kem():

    finding = make_finding("ECDH")

    target = MigrationPlanner().plan(
        finding
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

    assert (
        target.candidate_standard
        == "NIST FIPS 203"
    )

def test_rsa_without_usage_is_unresolved():

    finding = make_finding("RSA")

    target = MigrationPlanner().plan(
        finding
    )

    assert (
        target.purpose
        == CryptoPurpose.UNKNOWN
    )

    assert (
        target.migration_family
        == "UNRESOLVED"
    )

    assert target.candidate_algorithm is None
    assert target.candidate_standard is None

def test_ecc_without_usage_is_unresolved():

    finding = make_finding("ECC")

    target = MigrationPlanner().plan(
        finding
    )

    assert (
        target.purpose
        == CryptoPurpose.UNKNOWN
    )

    assert (
        target.migration_family
        == "UNRESOLVED"
    )

def test_aes_does_not_receive_pqc_target():

    finding = make_finding("AES")

    target = MigrationPlanner().plan(
        finding
    )

    assert (
        target.purpose
        == CryptoPurpose.UNKNOWN
    )

    assert (
        target.migration_family
        == "UNRESOLVED"
    )

    assert target.candidate_algorithm is None