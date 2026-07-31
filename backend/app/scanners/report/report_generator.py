from pathlib import Path

from app.scanners.findings import Finding
from app.scanners.report.report_summary import ReportSummary
from app.scanners.report.risk_calculator import RiskCalculator


class ReportGenerator:
    """
    Generates the complete security report.
    """

    def generate(
        self,
        files: list[Path],
        findings: list[Finding],
    ) -> dict:

        summary = ReportSummary().generate(
            files,
            findings,
        )

        risk = RiskCalculator().calculate(
            findings,
        )

        return {
            "summary": summary,
            "risk": risk,
            "findings": [
                {
                    "algorithm": finding.algorithm,
                    "file": finding.file_path,
                    "line": finding.line_number,
                    "severity": finding.severity,
                    "message": finding.message,
                    "recommendation": finding.recommendation,
                    "reference": finding.reference,
                }
                for finding in findings
            ],
        }