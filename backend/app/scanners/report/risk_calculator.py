from app.scanners.findings import Finding
from app.scanners.severity import Severity


class RiskCalculator:
    """
    Calculates overall scan risk.
    """

    def calculate(
        self,
        findings: list[Finding],
    ) -> dict:

        severity_count = {
            severity.value: 0
            for severity in Severity
        }

        for finding in findings:
            severity = finding.severity
            severity_count[severity] = severity_count.get(severity, 0) + 1

        if severity_count[Severity.CRITICAL.value]:
            overall_risk = Severity.CRITICAL.value

        elif severity_count[Severity.HIGH.value]:
            overall_risk = Severity.HIGH.value

        elif severity_count[Severity.MEDIUM.value]:
            overall_risk = Severity.MEDIUM.value

        elif severity_count[Severity.LOW.value]:
            overall_risk = Severity.LOW.value

        else:
            overall_risk = Severity.INFO.value

        return {
            "overall_risk": overall_risk,
            "severity_count": severity_count,
        }