from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity

class SHA224Rule(BaseCryptoRule):

    algorithm = "SHA-224"

    function_name = "sha224"

    allowed_modules = ("hashlib",)

    severity = Severity.INFO

    status = "APPROVED"

    message = "SHA-224 detected."

    recommendation = (
        "Review usage according to the application's "
        "security requirements."
    )

    reference = "NIST FIPS 180-4"