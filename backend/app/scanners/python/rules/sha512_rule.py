from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity
from app.taxonomy.crypto_taxonomy import (
    CryptoAlgorithm,
    FindingSeverity,
    CryptoStatus,
)
class SHA512Rule(BaseCryptoRule):

    algorithm = CryptoAlgorithm.SHA512

    function_name = "sha512"

    allowed_modules = ("hashlib",)

    severity = FindingSeverity.INFO

    status = CryptoStatus.APPROVED

    message = "SHA-512 detected."

    recommendation = "No immediate action required."

    reference = "NIST FIPS 180-4"