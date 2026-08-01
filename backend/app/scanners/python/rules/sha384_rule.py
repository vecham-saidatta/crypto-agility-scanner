from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity


class SHA384Rule(BaseCryptoRule):

    algorithm = "SHA-384"
    
    function_name = "sha384"

    allowed_modules = ("hashlib",)

    severity = Severity.INFO

    status = "APPROVED"

    message = "SHA-384 detected."

    recommendation = "No immediate action required."

    reference = "NIST FIPS 180-4"