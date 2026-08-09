from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity
from app.taxonomy.crypto_taxonomy import (
    CryptoAlgorithm,
    FindingSeverity,
    CryptoStatus,
)
class SHA224Rule(BaseCryptoRule):

    algorithm = CryptoAlgorithm.SHA224

    function_name = "sha224"

    allowed_modules = ("hashlib",)

    severity = FindingSeverity.INFO

    status = CryptoStatus.APPROVED

    message = "SHA-224 detected."

    recommendation = (
        "Review usage according to the application's "
        "security requirements."
    )

    reference = "NIST FIPS 180-4"