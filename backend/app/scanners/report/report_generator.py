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

        # 1. Generate existing summary
        summary = ReportSummary().generate(
            files,
            findings,
        )

        # 2. Calculate overall security risk
        risk = RiskCalculator().calculate(
            findings,
        )

        # 3. Separate real security findings
        # from informational crypto detections
        security_findings = [
            finding
            for finding in findings
            if finding.severity != "INFO"
        ]

        # 4. Count approved cryptography
        approved_crypto = [
            finding
            for finding in findings
            if finding.status == "APPROVED"
        ]

        # 5. Add the new metrics INTO the summary dictionary
        summary["crypto_inventory_count"] = len(findings)

        summary["security_findings_count"] = len(
            security_findings
        )

        summary["approved_crypto_count"] = len(
            approved_crypto
        )

        # 6. Build algorithm inventory
        algorithm_inventory = {}

        for finding in findings:
            algorithm_inventory[finding.algorithm] = (
                algorithm_inventory.get(
                    finding.algorithm,
                    0,
                )
                + 1
            )

        # 7. Generate final report
        return {
            "summary": summary,
            "risk": risk,
            "algorithm_inventory": algorithm_inventory,
            "findings": [
                {
                    "algorithm": finding.algorithm,
                    "file": finding.file_path,
                    "line": finding.line_number,
                    "severity": finding.severity,
                    "status": finding.status,
                    "message": finding.message,
                    "recommendation": finding.recommendation,
                    "reference": finding.reference,
                }
                for finding in findings
            ],
        }