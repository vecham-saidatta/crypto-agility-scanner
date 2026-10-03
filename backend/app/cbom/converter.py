from app.cbom.cbom import CBOM
from app.cbom.component import CBOMComponent
from app.scanners.findings import Finding
class CBOMConverter:
    """
    Converts scanner findings into CBOM components.
    """
    def from_finding(
        self,
        finding: Finding,
    ) -> CBOMComponent:
        return CBOMComponent(
            algorithm=finding.algorithm,
            file=finding.file_path,
            line=finding.line_number,
            properties=finding.metadata.copy(),
        )
    def from_findings(
        self,
        findings: list[Finding],
    ) -> list[CBOMComponent]:
        return [
            self.from_finding(finding)
            for finding in findings
        ]
    def convert(
        self,
        findings: list[Finding],
    ) -> CBOM:
        components = self.from_findings(
            findings
        )

        return CBOM(
            components=components
        )