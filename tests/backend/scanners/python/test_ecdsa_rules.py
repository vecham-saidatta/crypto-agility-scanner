from pathlib import Path

from app.scanners.python.python_scanner import (
    PythonScanner,
)
from cryptography.hazmat.primitives import hashes as crypto_hashes
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.hashes import SHA256
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

def test_detects_ecdsa_sha256(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

signature_algorithm = ec.ECDSA(
    hashes.SHA256()
)
""",
    )

    ecdsa_findings = [
        finding
        for finding in findings
        if finding.algorithm == "ECDSA"
    ]

    assert len(ecdsa_findings) == 1

    assert (
        ecdsa_findings[0]
        .metadata["hash_algorithm"]
        == "SHA-256"
    )

def test_extracts_ecdsa_sha384(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec

algorithm = ec.ECDSA(
    hashes.SHA384()
)
""",
    )

    finding = next(
        finding
        for finding in findings
        if finding.algorithm == "ECDSA"
    )

    assert (
        finding.metadata["hash_algorithm"]
        == "SHA-384"
    )

def test_detects_ecdsa_ec_alias(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec as elliptic

algorithm = elliptic.ECDSA(
    hashes.SHA256()
)
""",
    )

    assert any(
        finding.algorithm == "ECDSA"
        for finding in findings
    )

def test_detects_ecdsa_hash_alias(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives import hashes as crypto_hashes
from cryptography.hazmat.primitives.asymmetric import ec

algorithm = ec.ECDSA(
    crypto_hashes.SHA512()
)
""",
    )

    finding = next(
        finding
        for finding in findings
        if finding.algorithm == "ECDSA"
    )

    assert (
        finding.metadata["hash_algorithm"]
        == "SHA-512"
    )

def test_detects_direct_ecdsa_import(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric.ec import ECDSA
from cryptography.hazmat.primitives.hashes import SHA256

algorithm = ECDSA(
    SHA256()
)
""",
    )

    finding = next(
        finding
        for finding in findings
        if finding.algorithm == "ECDSA"
    )

    assert (
        finding.metadata["hash_algorithm"]
        == "SHA-256"
    )

def test_ignores_fake_ecdsa(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
class FakeEC:

    def ECDSA(self, algorithm):
        return algorithm


class FakeHashes:

    def SHA256(self):
        return "fake"


ec = FakeEC()
hashes = FakeHashes()

algorithm = ec.ECDSA(
    hashes.SHA256()
)
""",
    )

    assert not any(
        finding.algorithm == "ECDSA"
        for finding in findings
    )

def test_handles_dynamic_ecdsa_hash(
    tmp_path,
):

    findings = scan_source(
        tmp_path,
        """
from cryptography.hazmat.primitives.asymmetric import ec

hash_algorithm = choose_hash()

algorithm = ec.ECDSA(
    hash_algorithm
)
""",
    )

    finding = next(
        finding
        for finding in findings
        if finding.algorithm == "ECDSA"
    )

    assert (
        finding.metadata["hash_algorithm"]
        is None
    )