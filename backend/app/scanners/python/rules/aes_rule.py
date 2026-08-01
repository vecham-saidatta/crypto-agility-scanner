from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity


class AESRule(BaseCryptoRule):

    algorithm = "AES"
    
    function_name = "AES"

    allowed_modules = (
        "cryptography.hazmat.primitives.ciphers.algorithms",
    )

    severity = Severity.INFO

    status = "APPROVED"

    message = "AES detected."

    recommendation = (
        "Review key size, cipher mode, nonce/IV handling, "
        "and authentication configuration."
    )

    reference = "NIST FIPS 197"