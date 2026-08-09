from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity
from app.taxonomy.crypto_taxonomy import (
    CryptoAlgorithm,
    FindingSeverity,
    CryptoStatus,
)

class SHA256Rule(BaseCryptoRule):
    """
    Detects SHA-256 usage.
    """

    algorithm = CryptoAlgorithm.SHA256

    function_name = "sha256"

    allowed_modules = ("hashlib",)

    severity = FindingSeverity.INFO

    status = CryptoStatus.APPROVED

    message = "SHA-256 detected."

    recommendation = "No action required."

    reference = "NIST FIPS 180-4"