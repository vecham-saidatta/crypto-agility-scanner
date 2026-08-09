from app.assessment.assessment_result import (
    CryptoAssessmentResult,
)
from app.assessment.policies.rsa_policy import RSAPolicy
from app.assessment.policies.ecc_policy import ECCPolicy
from app.scanners.findings import Finding
from app.assessment.policies.ecdsa_policy import (
    ECDSAPolicy,
)
from app.assessment.policies.ecdh_policy import (
    ECDHPolicy,
)
from app.assessment.policies.rsa_signature_policy import (
    RSASignaturePolicy,
)
from app.assessment.policies.rsa_encryption_policy import (
    RSAEncryptionPolicy,
)


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

            return RSAPolicy().assess(
                key_size=key_size
            )

        if finding.algorithm == "RSA-SIGNATURE":

            hash_algorithm = finding.metadata.get(
                "hash_algorithm"
            )

            padding = finding.metadata.get(
                "padding"
            )

            return RSASignaturePolicy().assess(
                hash_algorithm=hash_algorithm,
                padding=padding,
            )

        if finding.algorithm == "RSA-ENCRYPTION":

            padding = finding.metadata.get(
                "padding"
            )

            hash_algorithm = finding.metadata.get(
                "hash_algorithm"
            )

            return RSAEncryptionPolicy().assess(
                padding=padding,
                hash_algorithm=hash_algorithm,
            )

        if finding.algorithm == "ECC":

            curve = finding.metadata.get(
                "curve"
            )

            return ECCPolicy().assess(
                curve=curve
            )

        if finding.algorithm == "ECDSA":

            hash_algorithm = finding.metadata.get(
                "hash_algorithm"
            )

            return ECDSAPolicy().assess(
                hash_algorithm=hash_algorithm
            )

        if finding.algorithm == "ECDH":

            return ECDHPolicy().assess()

        return None