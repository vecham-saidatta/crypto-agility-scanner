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


def test_detects_hashlib_md5(tmp_path):

    findings = scan_source(
        tmp_path,
        """
import hashlib

result = hashlib.md5(b"hello")
""",
    )

    md5_findings = [
        finding
        for finding in findings
        if finding.algorithm == "MD5"
    ]

    assert len(md5_findings) == 1
    assert md5_findings[0].severity == "HIGH"
    assert md5_findings[0].status == "DEPRECATED"


def test_detects_direct_md5_import(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from hashlib import md5

result = md5(b"hello")
""",
    )

    assert any(
        finding.algorithm == "MD5"
        for finding in findings
    )


def test_detects_hashlib_alias(tmp_path):

    findings = scan_source(
        tmp_path,
        """
import hashlib as hl

result = hl.md5(b"hello")
""",
    )

    assert any(
        finding.algorithm == "MD5"
        for finding in findings
    )


def test_ignores_local_md5_function(tmp_path):

    findings = scan_source(
        tmp_path,
        """
def md5(data):
    return data

result = md5(b"hello")
""",
    )

    assert not any(
        finding.algorithm == "MD5"
        for finding in findings
    )


def test_import_shadowing(tmp_path):

    findings = scan_source(
        tmp_path,
        """
from hashlib import md5

real_hash = md5(b"real")

def md5(data):
    return data

fake_hash = md5(b"fake")
""",
    )

    md5_findings = [
        finding
        for finding in findings
        if finding.algorithm == "MD5"
    ]

    assert len(md5_findings) == 1


def test_ignores_unrelated_md5_method(tmp_path):

    findings = scan_source(
        tmp_path,
        """
class FakeCrypto:

    def md5(self, data):
        return data


crypto = FakeCrypto()

result = crypto.md5(b"hello")
""",
    )

    assert not any(
        finding.algorithm == "MD5"
        for finding in findings
    )