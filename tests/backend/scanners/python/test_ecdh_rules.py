from pathlib import Path

from app.scanners.python.python_scanner import (
    PythonScanner,
)


def scan_source(
    tmp_path: Path,
    source: str,
):

    test_file = tmp_path / "sample.py"

    test_file.write_text(
        source,
        encoding="utf-8",
    )

    return PythonScanner().scan(
        [test_file]
    )

def test_detects_ecdh(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import ec

algorithm = ec.ECDH()
""",
    )

    ecdh_findings = [
        finding
        for finding in findings
        if finding.algorithm == "ECDH"
    ]

    assert len(ecdh_findings) == 1

    assert (
        ecdh_findings[0].status
        == "QUANTUM_VULNERABLE"
    )

def test_ecdh_records_key_agreement_operation(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import ec

algorithm = ec.ECDH()
""",
    )

    finding = next(
        finding
        for finding in findings
        if finding.algorithm == "ECDH"
    )

    assert (
        finding.metadata["operation"]
        == "key_agreement"
    )

def test_detects_ecdh_import_alias(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import ec as elliptic

algorithm = elliptic.ECDH()
""",
    )

    assert any(
        finding.algorithm == "ECDH"
        for finding in findings
    )

def test_detects_direct_ecdh_import(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric.ec import ECDH

algorithm = ECDH()
""",
    )

    assert any(
        finding.algorithm == "ECDH"
        for finding in findings
    )

def test_detects_direct_ecdh_alias(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric.ec import ECDH as KeyAgreement

algorithm = KeyAgreement()
""",
    )

    assert any(
        finding.algorithm == "ECDH"
        for finding in findings
    )

def test_ignores_fake_ecdh(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
class FakeEC:

    def ECDH(self):
        return "fake"


ec = FakeEC()

algorithm = ec.ECDH()
""",
    )

    assert not any(
        finding.algorithm == "ECDH"
        for finding in findings
    )