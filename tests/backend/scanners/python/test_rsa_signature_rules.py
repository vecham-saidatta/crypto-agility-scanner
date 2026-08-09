from pathlib import Path

from app.scanners.python.python_scanner import PythonScanner


def scan_source(
    tmp_path,
    source: str,
):

    file_path = (
        tmp_path / "example.py"
    )

    file_path.write_text(
        source,
        encoding="utf-8",
    )

    scanner = PythonScanner()

    return scanner.scan(
        [file_path]
    )

def test_detects_rsa_pss_signature(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

private_key.sign(
    b"message",
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH,
    ),
    hashes.SHA256(),
)
""",
    )

    rsa_findings = [
        finding
        for finding in findings
        if finding.algorithm == "RSA-SIGNATURE"
    ]

    assert len(rsa_findings) == 1

    finding = rsa_findings[0]

    assert finding.metadata["operation"] == "SIGN"
    assert finding.metadata["padding"] == "PSS"

    assert (
        finding.metadata["hash_algorithm"]
        == "SHA-256"
    )
def test_detects_rsa_pkcs1v15_signature(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

private_key.sign(
    b"message",
    padding.PKCS1v15(),
    hashes.SHA384(),
)
""",
    )

    finding = next(
        finding
        for finding in findings
        if finding.algorithm == "RSA-SIGNATURE"
    )

    assert (
        finding.metadata["padding"]
        == "PKCS1v15"
    )

    assert (
        finding.metadata["hash_algorithm"]
        == "SHA-384"
    )

def test_detects_rsa_signature_padding_alias(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as pad

private_key.sign(
    b"message",
    pad.PKCS1v15(),
    hashes.SHA256(),
)
""",
    )

    assert any(
        finding.algorithm == "RSA-SIGNATURE"
        for finding in findings
    )

def test_detects_direct_pss_import(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import PSS, MGF1

private_key.sign(
    b"message",
    PSS(
        mgf=MGF1(hashes.SHA256()),
        salt_length=32,
    ),
    hashes.SHA256(),
)
""",
    )

    assert any(
        finding.algorithm == "RSA-SIGNATURE"
        for finding in findings
    )

def test_detects_rsa_signature_hash_alias(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes as h
from cryptography.hazmat.primitives.asymmetric import padding

private_key.sign(
    b"message",
    padding.PKCS1v15(),
    h.SHA512(),
)
""",
    )

    finding = next(
        finding
        for finding in findings
        if finding.algorithm == "RSA-SIGNATURE"
    )

    assert (
        finding.metadata["hash_algorithm"]
        == "SHA-512"
    )

def test_ignores_unrelated_sign_method(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
class Document:

    def sign(self, data):
        return data


document = Document()

document.sign(b"hello")
""",
    )

    assert not any(
        finding.algorithm == "RSA-SIGNATURE"
        for finding in findings
    )

