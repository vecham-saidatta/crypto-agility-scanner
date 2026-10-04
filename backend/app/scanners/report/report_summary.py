from pathlib import Path

from app.scanners.findings import Finding


class ReportSummary:
    def generate(
        self,
        files: list[Path],
        findings: list[Finding],
    ) -> dict:

        languages = set()

        for file in files:
            if file.suffix == ".py":
                languages.add("python")

            elif file.suffix == ".java":
                languages.add("java")

            elif file.suffix in {
                ".yaml",
                ".yml",
                ".json",
                ".toml",
                ".ini",
                ".conf",
            } or file.name in {
                "Dockerfile",
                "docker-compose.yml",
            }:
                languages.add("config")

        return {
            "files_scanned": len(files),
            "languages_detected": sorted(languages),
            "total_findings": len(findings),
        }