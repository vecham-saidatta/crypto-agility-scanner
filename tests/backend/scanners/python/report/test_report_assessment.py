from pathlib import Path

from app.scanners.findings import Finding
from app.scanners.report.report_generator import (
    ReportGenerator,
)


def create_rsa_finding(
    key_size: int | None = 2048,
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


def test_report_contains_rsa_assessment():

    finding = create_rsa_finding()

    report = ReportGenerator().generate(
        files=[Path("example.py")],
        findings=[finding],
    )

    rsa_finding = report["findings"][0]

    assessment = rsa_finding["assessment"]

    assert assessment is not None

    assert (
        assessment["classical_security"]["status"]
        == "ACCEPTABLE"
    )

    assert (
        assessment["quantum_security"]["vulnerable"]
        is True
    )

    assert (
        assessment["migration"]["required"]
        is True
    )


def test_report_counts_quantum_vulnerable_crypto():

    finding = create_rsa_finding()

    report = ReportGenerator().generate(
        files=[Path("example.py")],
        findings=[finding],
    )

    assert (
        report["summary"]["quantum_vulnerable_count"]
        == 1
    )

    assert (
        report["summary"]["migration_required_count"]
        == 1
    )


def test_report_handles_non_assessed_algorithm():

    finding = Finding(
        algorithm="SHA-256",
        file_path="example.py",
        line_number=5,
        severity="INFO",
        status="APPROVED",
        message="SHA-256 detected.",
        recommendation="No action required.",
        reference="NIST FIPS 180-4",
        metadata={},
    )

    report = ReportGenerator().generate(
        files=[Path("example.py")],
        findings=[finding],
    )

    assert (
        report["findings"][0]["assessment"]
        is None
    )

    assert (
        report["summary"]["quantum_vulnerable_count"]
        == 0
    )

    assert (
        report["summary"]["migration_required_count"]
        == 0
    )


def test_report_assesses_weak_rsa():

    finding = create_rsa_finding(
        key_size=1024
    )

    report = ReportGenerator().generate(
        files=[Path("example.py")],
        findings=[finding],
    )

    assessment = (
        report["findings"][0]["assessment"]
    )

    assert (
        assessment["classical_security"]["status"]
        == "DISALLOWED"
    )

    assert (
        assessment["classical_security"]["risk"]
        == "HIGH"
    )