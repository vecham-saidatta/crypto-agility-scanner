from app.assessment.assessment_result import (
    CryptoAssessmentResult,
)
from app.assessment.policies.rsa_policy import RSAPolicy
from app.scanners.findings import Finding


class CryptoAssessor:
    """
    Selects the appropriate cryptographic policy
    and assesses scanner findings.
    """

    def assess(
        self,
        finding: Finding,
    ) -> CryptoAssessmentResult | None:

        if finding.algorithm == "RSA":

            key_size = finding.metadata.get(
                "key_size"
            )

            policy = RSAPolicy()

            return policy.assess(
                key_size=key_size
            )

        return None