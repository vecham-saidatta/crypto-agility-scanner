from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity


class SHA256Rule(BaseCryptoRule):
    """
    Detects SHA-256 usage.
    """

    algorithm = "SHA-256"

    function_name = "sha256"

    allowed_modules = ("hashlib",)

    severity = Severity.INFO

    status = "APPROVED"

    message = "SHA-256 detected."

    recommendation = "No action required."

    reference = "NIST FIPS 180-4"