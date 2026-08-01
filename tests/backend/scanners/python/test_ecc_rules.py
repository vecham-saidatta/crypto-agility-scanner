from pathlib import Path

from app.scanners.python.python_scanner import PythonScanner

from cryptography.hazmat.primitives.asymmetric.ec import (
    generate_private_key,
    SECP521R1,
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

    scanner = PythonScanner()

    return scanner.scan([test_file])

def test_detects_ecc_key_generation(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import ec

private_key = ec.generate_private_key(
    ec.SECP256R1()
)
""",
    )

    ecc_findings = [
        finding
        for finding in findings
        if finding.algorithm == "ECC"
    ]

    assert len(ecc_findings) == 1

    assert (
        ecc_findings[0].metadata["curve"]
        == "SECP256R1"
    )

def test_extracts_secp384r1_curve(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import ec

private_key = ec.generate_private_key(
    ec.SECP384R1()
)
""",
    )

    ecc_finding = next(
        finding
        for finding in findings
        if finding.algorithm == "ECC"
    )

    assert (
        ecc_finding.metadata["curve"]
        == "SECP384R1"
    )

def test_detects_ecc_import_alias(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import ec as elliptic

private_key = elliptic.generate_private_key(
    elliptic.SECP256R1()
)
""",
    )

    ecc_finding = next(
        finding
        for finding in findings
        if finding.algorithm == "ECC"
    )

    assert (
        ecc_finding.metadata["curve"]
        == "SECP256R1"
    )


def test_detects_direct_ecc_import(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric.ec import (
    generate_private_key,
    SECP521R1,
)

private_key = generate_private_key(
    SECP521R1()
)
""",
    )

    ecc_finding = next(
        finding
        for finding in findings
        if finding.algorithm == "ECC"
    )

    assert (
        ecc_finding.metadata["curve"]
        == "SECP521R1"
    )

def test_ignores_fake_ecc_generation(tmp_path):

    findings = scan_source(
        tmp_path,
        """
class FakeEC:

    def generate_private_key(self, curve):
        return "fake"


class SECP256R1:
    pass


ec = FakeEC()

key = ec.generate_private_key(
    SECP256R1()
)
""",
    )

    assert not any(
        finding.algorithm == "ECC"
        for finding in findings
    )

def test_handles_dynamic_ecc_curve(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import ec

curve = get_curve()

private_key = ec.generate_private_key(
    curve
)
""",
    )

    ecc_finding = next(
        finding
        for finding in findings
        if finding.algorithm == "ECC"
    )

    assert (
        ecc_finding.metadata["curve"]
        is None
    )

def test_ecc_uses_correct_nist_reference(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import ec

private_key = ec.generate_private_key(
    ec.SECP256R1()
)
""",
    )

    ecc_finding = next(
        finding
        for finding in findings
        if finding.algorithm == "ECC"
    )

    assert (
        ecc_finding.reference
        == "NIST SP 800-186"
    )