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


def test_detects_aes(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.ciphers import algorithms

key = b"0" * 32
cipher = algorithms.AES(key)
""",
    )

    aes_findings = [
        finding
        for finding in findings
        if finding.algorithm == "AES"
    ]

    assert len(aes_findings) == 1
    assert aes_findings[0].severity == "INFO"
    assert aes_findings[0].status == "APPROVED"


def test_detects_direct_aes_import(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.ciphers.algorithms import AES

cipher = AES(b"0" * 32)
""",
    )

    assert any(
        finding.algorithm == "AES"
        for finding in findings
    )


def test_detects_triple_des(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.ciphers import algorithms

cipher = algorithms.TripleDES(b"0" * 24)
""",
    )

    triple_des_findings = [
        finding
        for finding in findings
        if finding.algorithm == "TripleDES"
    ]

    assert len(triple_des_findings) == 1
    assert triple_des_findings[0].severity == "HIGH"
    assert triple_des_findings[0].status == "DEPRECATED"


def test_detects_rc4(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.ciphers import algorithms

cipher = algorithms.ARC4(b"0" * 16)
""",
    )

    rc4_findings = [
        finding
        for finding in findings
        if finding.algorithm == "RC4"
    ]

    assert len(rc4_findings) == 1
    assert rc4_findings[0].severity == "HIGH"
    assert rc4_findings[0].status == "DEPRECATED"


def test_detects_chacha20(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.ciphers import algorithms

key = b"0" * 32
nonce = b"0" * 16

cipher = algorithms.ChaCha20(key, nonce)
""",
    )

    findings = [
        finding
        for finding in findings
        if finding.algorithm == "ChaCha20"
    ]

    assert len(findings) == 1
    assert findings[0].severity == "INFO"
    assert findings[0].status == "APPROVED"


def test_ignores_fake_aes(tmp_path):

    findings = scan_source(
        tmp_path,
        """
class AES:
    pass

cipher = AES()
""",
    )

    assert not any(
        finding.algorithm == "AES"
        for finding in findings
    )