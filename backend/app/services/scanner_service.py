from pathlib import Path

from app.scanners.discovery.file_discovery import FileDiscovery
from app.scanners.discovery.language_detector import LanguageDetector
from app.scanners.scanner_registry import ScannerRegistry
from app.scanners.report.report_generator import ReportGenerator


class ScannerService:
    """
    Coordinates the complete repository scanning pipeline.
    """

    def scan(
        self,
        repository_path: str | Path,
    ) -> dict:
        """
        Scan a local repository and generate a security report.

        Pipeline:
        1. Discover files.
        2. Detect languages.
        3. Run registered scanners.
        4. Generate security report.
        """

        repository_path = Path(repository_path)

        discovery = FileDiscovery()

        files = discovery.discover_files(
            repository_path
        )

        detector = LanguageDetector()

        grouped_files = detector.detect_languages(
            files
        )

        registry = ScannerRegistry()

        findings = registry.scan(
            grouped_files
        )

        report_generator = ReportGenerator()

        report = report_generator.generate(
            files,
            findings,
        )

        return report