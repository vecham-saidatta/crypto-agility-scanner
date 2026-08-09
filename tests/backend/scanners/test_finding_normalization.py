from app.scanners.findings import Finding


def make_finding(
    algorithm: str,
    severity: str,
    status: str,
) -> Finding:

    return Finding(
        algorithm=algorithm,
        file_path="example.py",
        line_number=10,
        severity=severity,
        status=status,
        message="Test finding.",
        recommendation="Test recommendation.",
        reference="Test reference.",
        metadata={},
    )


def test_finding_normalizes_algorithm():

    finding = make_finding(
        algorithm="rsa_signature",
        severity="INFO",
        status="QUANTUM_VULNERABLE",
    )

    assert (
        finding.algorithm
        == "RSA-SIGNATURE"
    )


def test_finding_normalizes_severity():

    finding = make_finding(
        algorithm="RSA",
        severity="high",
        status="DEPRECATED",
    )

    assert finding.severity == "HIGH"


def test_finding_normalizes_status():

    finding = make_finding(
        algorithm="RSA",
        severity="INFO",
        status="quantum_vulnerable",
    )

    assert (
        finding.status
        == "QUANTUM_VULNERABLE"
    )


def test_finding_preserves_existing_values():

    finding = make_finding(
        algorithm="ECDSA",
        severity="INFO",
        status="QUANTUM_VULNERABLE",
    )

    assert finding.algorithm == "ECDSA"
    assert finding.severity == "INFO"

    assert (
        finding.status
        == "QUANTUM_VULNERABLE"
    )