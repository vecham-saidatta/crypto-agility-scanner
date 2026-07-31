from pathlib import Path

from app.scanners.findings import Finding


class ReportSummary:
    """
    Responsible for generating scan summary statistics.
    """

    def generate(
        self,
        files: list[Path],
        findings: list[Finding],
    ) -> dict:

        languages = {
            file.suffix
            for file in files
            if file.suffix
        }

        return {
            "files_scanned": len(files),
            "languages_detected": sorted(languages),
            "total_findings": len(findings),
        }