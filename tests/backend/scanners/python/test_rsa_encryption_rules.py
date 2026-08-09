from pathlib import Path

from app.scanners.python.python_scanner import (
    PythonScanner,
)


def scan_source(
    tmp_path: Path,
    source: str,
):
    """
    Creates a temporary Python source file
    and scans it using PythonScanner.
    """

    file_path = tmp_path / "example.py"

    file_path.write_text(
        source,
        encoding="utf-8",
    )

    scanner = PythonScanner()

    # IMPORTANT:
    # PythonScanner.scan() expects a LIST of files.
    return scanner.scan(
        [file_path]
    )


def test_detects_rsa_oaep_encryption(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

ciphertext = public_key.encrypt(
    b"message",
    padding.OAEP(
        mgf=padding.MGF1(
            algorithm=hashes.SHA256()
        ),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)
""",
    )

    rsa_findings = [
        finding
        for finding in findings
        if finding.algorithm == "RSA-ENCRYPTION"
    ]

    assert len(rsa_findings) == 1

    finding = rsa_findings[0]

    assert (
        finding.metadata["operation"]
        == "ENCRYPT"
    )

    assert (
        finding.metadata["padding"]
        == "OAEP"
    )

    assert (
        finding.metadata["hash_algorithm"]
        == "SHA-256"
    )


def test_detects_rsa_oaep_decryption(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(
            algorithm=hashes.SHA256()
        ),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)
""",
    )

    rsa_findings = [
        finding
        for finding in findings
        if finding.algorithm == "RSA-ENCRYPTION"
    ]

    assert len(rsa_findings) == 1

    finding = rsa_findings[0]

    assert (
        finding.metadata["operation"]
        == "DECRYPT"
    )

    assert (
        finding.metadata["padding"]
        == "OAEP"
    )

    assert (
        finding.metadata["hash_algorithm"]
        == "SHA-256"
    )


def test_detects_rsa_pkcs1v15_encryption(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import padding

ciphertext = public_key.encrypt(
    b"message",
    padding.PKCS1v15(),
)
""",
    )

    rsa_findings = [
        finding
        for finding in findings
        if finding.algorithm == "RSA-ENCRYPTION"
    ]

    assert len(rsa_findings) == 1

    finding = rsa_findings[0]

    assert (
        finding.metadata["operation"]
        == "ENCRYPT"
    )

    assert (
        finding.metadata["padding"]
        == "PKCS1v15"
    )

    assert (
        finding.metadata["hash_algorithm"]
        is None
    )


def test_detects_rsa_encryption_padding_alias(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding as pad

ciphertext = public_key.encrypt(
    b"message",
    pad.OAEP(
        mgf=pad.MGF1(
            algorithm=hashes.SHA384()
        ),
        algorithm=hashes.SHA384(),
        label=None,
    ),
)
""",
    )

    rsa_findings = [
        finding
        for finding in findings
        if finding.algorithm == "RSA-ENCRYPTION"
    ]

    assert len(rsa_findings) == 1

    finding = rsa_findings[0]

    assert (
        finding.metadata["padding"]
        == "OAEP"
    )

    assert (
        finding.metadata["hash_algorithm"]
        == "SHA-384"
    )


def test_detects_direct_oaep_import(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1

ciphertext = public_key.encrypt(
    b"message",
    OAEP(
        mgf=MGF1(
            algorithm=hashes.SHA256()
        ),
        algorithm=hashes.SHA256(),
        label=None,
    ),
)
""",
    )

    rsa_findings = [
        finding
        for finding in findings
        if finding.algorithm == "RSA-ENCRYPTION"
    ]

    assert len(rsa_findings) == 1

    finding = rsa_findings[0]

    assert (
        finding.metadata["padding"]
        == "OAEP"
    )

    assert (
        finding.metadata["hash_algorithm"]
        == "SHA-256"
    )


def test_ignores_unrelated_encrypt_method(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
class CustomCipher:

    def encrypt(self, data):
        return data


cipher = CustomCipher()

cipher.encrypt(b"hello")
""",
    )

    rsa_findings = [
        finding
        for finding in findings
        if finding.algorithm == "RSA-ENCRYPTION"
    ]

    assert rsa_findings == []