from pathlib import Path
import json
from app.scanners.discovery.file_discovery import FileDiscovery
from app.scanners.discovery.language_detector import LanguageDetector
from app.scanners.scanner_registry import ScannerRegistry
from app.scanners.report.report_generator import ReportGenerator


def main():

    repository_path = Path("test_repository")

    print("=" * 60)
    print("Crypto Agility Scanner")
    print("=" * 60)

    # Step 1
    discovery = FileDiscovery()
    files = discovery.discover_files(repository_path)

    print(f"Files discovered: {len(files)}")

    # Step 2
    detector = LanguageDetector()
    grouped_files = detector.detect_languages(files)

    print()

    print("Detected Languages")

    for language, language_files in grouped_files.items():
        print(f"{language}: {len(language_files)} files")

    # Step 3
    registry = ScannerRegistry()
    findings = registry.scan(grouped_files)

    print()

    report_generator = ReportGenerator()

    report = report_generator.generate(
        files,
        findings,
    )

    print("=" * 60)
    print("Security Report")
    print("=" * 60)

    print(
        json.dumps(
            report,
            indent=4,
        )
    )


if __name__ == "__main__":
    main()