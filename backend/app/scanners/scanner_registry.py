from pathlib import Path

from app.scanners.findings import Finding

from app.scanners.python.python_scanner import PythonScanner
from app.scanners.java.java_scanner import JavaScanner
from app.scanners.config.config_scanner import ConfigScanner


class ScannerRegistry:
    """
    Responsible for dispatching files to the correct scanner.
    """

    def scan(
        self,
        grouped_files: dict[str, list[Path]],
    ) -> list[Finding]:

        findings: list[Finding] = []

        scanners = {
            "python": PythonScanner(),
            "java": JavaScanner(),
            "config": ConfigScanner(),
        }

        for language, files in grouped_files.items():

            scanner = scanners.get(language)

            if scanner is None:
                continue

            findings.extend(
                scanner.scan(files)
            )

        return findings