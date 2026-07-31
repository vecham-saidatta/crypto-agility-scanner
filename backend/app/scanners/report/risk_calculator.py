from app.scanners.findings import Finding


class RiskCalculator:
    """
    Calculates overall scan risk.
    """

    def calculate(
        self,
        findings: list[Finding],
    ) -> dict:

        severity_count = {
            "CRITICAL": 0,
            "HIGH": 0,
            "MEDIUM": 0,
            "LOW": 0,
        }

        for finding in findings:
            severity_count[finding.severity] += 1

        if severity_count["CRITICAL"] > 0:
            overall_risk = "CRITICAL"

        elif severity_count["HIGH"] > 0:
            overall_risk = "HIGH"

        elif severity_count["MEDIUM"] > 0:
            overall_risk = "MEDIUM"

        else:
            overall_risk = "LOW"

        return {
            "overall_risk": overall_risk,
            "severity_count": severity_count,
        }