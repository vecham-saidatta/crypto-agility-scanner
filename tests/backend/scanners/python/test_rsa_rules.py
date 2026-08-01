from pathlib import Path

from app.scanners.python.python_scanner import PythonScanner


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


def test_detects_rsa_key_generation(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import rsa

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
""",
    )

    rsa_findings = [
        finding
        for finding in findings
        if finding.algorithm == "RSA"
    ]

    assert len(rsa_findings) == 1

    assert rsa_findings[0].status == (
        "QUANTUM_VULNERABLE"
    )

def test_detects_rsa_import_alias(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import rsa as rsa_crypto

private_key = rsa_crypto.generate_private_key(
    public_exponent=65537,
    key_size=3072,
)
""",
    )

    assert any(
        finding.algorithm == "RSA"
        for finding in findings
    )

def test_ignores_fake_rsa_generation(tmp_path):

    findings = scan_source(
        tmp_path,
        """
class FakeRSA:

    def generate_private_key(self):
        return "fake"


rsa = FakeRSA()

key = rsa.generate_private_key()
""",
    )

    rsa_findings = [
        finding
        for finding in findings
        if finding.algorithm == "RSA"
    ]

    assert len(rsa_findings) == 0

def test_extracts_rsa_3072_key_size(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import rsa

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=3072,
)
""",
    )

    rsa_finding = next(
        finding
        for finding in findings
        if finding.algorithm == "RSA"
    )

    assert rsa_finding.metadata["key_size"] == 3072

def test_handles_dynamic_rsa_key_size(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import rsa

RSA_KEY_SIZE = get_key_size()

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=RSA_KEY_SIZE,
)
""",
    )

    rsa_finding = next(
        finding
        for finding in findings
        if finding.algorithm == "RSA"
    )

    assert (
        rsa_finding.metadata["key_size"]
        is None
    )

    assert (
        rsa_finding.metadata["public_exponent"]
        == 65537
    )

def test_rsa_uses_correct_nist_reference(
    tmp_path,
):

    source = """
from cryptography.hazmat.primitives.asymmetric import rsa

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
)
"""

    test_file = tmp_path / "rsa_reference.py"

    test_file.write_text(
        source,
        encoding="utf-8",
    )

    findings = PythonScanner().scan(
        [test_file]
    )

    rsa_finding = next(
        finding
        for finding in findings
        if finding.algorithm == "RSA"
    )

    assert (
        rsa_finding.reference
        == "NIST FIPS 186-5"
    )