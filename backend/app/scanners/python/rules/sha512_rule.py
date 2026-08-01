from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity

class SHA512Rule(BaseCryptoRule):

    algorithm = "SHA-512"

    function_name = "sha512"

    allowed_modules = ("hashlib",)

    severity = Severity.INFO

    status = "APPROVED"

    message = "SHA-512 detected."

    recommendation = "No immediate action required."

    reference = "NIST FIPS 180-4"