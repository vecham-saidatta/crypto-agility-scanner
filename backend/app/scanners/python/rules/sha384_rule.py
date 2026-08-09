from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity
from app.taxonomy.crypto_taxonomy import (
    CryptoAlgorithm,
    FindingSeverity,
    CryptoStatus,
)

class SHA384Rule(BaseCryptoRule):

    algorithm = CryptoAlgorithm.SHA384
    
    function_name = "sha384"

    allowed_modules = ("hashlib",)

    severity = FindingSeverity.INFO

    status = CryptoStatus.APPROVED

    message = "SHA-384 detected."

    recommendation = "No immediate action required."

    reference = "NIST FIPS 180-4"