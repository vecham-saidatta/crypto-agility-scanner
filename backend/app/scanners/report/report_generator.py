from pathlib import Path

from app.scanners.findings import Finding
from app.scanners.report.report_summary import ReportSummary
from app.scanners.report.risk_calculator import RiskCalculator
from app.assessment.crypto_assessor import CryptoAssessor


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

        # 5. Add existing crypto metrics
        summary["crypto_inventory_count"] = len(
            findings
        )

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

        # 7. Create crypto assessment engine
        assessor = CryptoAssessor()

        quantum_vulnerable_count = 0
        migration_required_count = 0

        report_findings = []

        # 8. Assess and serialize every finding
        for finding in findings:

            assessment = assessor.assess(
                finding
            )

            assessment_data = None

            if assessment is not None:

                if (
                    assessment
                    .quantum_security
                    .vulnerable
                ):
                    quantum_vulnerable_count += 1

                if (
                    assessment
                    .migration
                    .required
                ):
                    migration_required_count += 1

                assessment_data = {
                    "classical_security": {
                        "status": (
                            assessment
                            .classical_security
                            .status
                        ),
                        "risk": (
                            assessment
                            .classical_security
                            .risk
                        ),
                        "message": (
                            assessment
                            .classical_security
                            .message
                        ),
                    },
                    "quantum_security": {
                        "status": (
                            assessment
                            .quantum_security
                            .status
                        ),
                        "risk": (
                            assessment
                            .quantum_security
                            .risk
                        ),
                        "vulnerable": (
                            assessment
                            .quantum_security
                            .vulnerable
                        ),
                        "message": (
                            assessment
                            .quantum_security
                            .message
                        ),
                    },
                    "migration": {
                        "required": (
                            assessment
                            .migration
                            .required
                        ),
                        "priority": (
                            assessment
                            .migration
                            .priority
                        ),
                        "recommendation": (
                            assessment
                            .migration
                            .recommendation
                        ),
                    },
                }

            report_findings.append(
                {
                    "algorithm": finding.algorithm,
                    "file": finding.file_path,
                    "line": finding.line_number,
                    "severity": finding.severity,
                    "status": finding.status,
                    "message": finding.message,
                    "recommendation": (
                        finding.recommendation
                    ),
                    "reference": finding.reference,
                    "metadata": finding.metadata,
                    "assessment": assessment_data,
                }
            )

        # 9. Add PQC metrics to summary
        summary["quantum_vulnerable_count"] = (
            quantum_vulnerable_count
        )

        summary["migration_required_count"] = (
            migration_required_count
        )

        # 10. Generate final report
        return {
            "summary": summary,
            "risk": risk,
            "algorithm_inventory": (
                algorithm_inventory
            ),
            "findings": report_findings,
        }