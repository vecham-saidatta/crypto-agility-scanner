from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity


class ChaCha20Rule(BaseCryptoRule):

    algorithm = "ChaCha20"

    function_name = "ChaCha20"

    allowed_modules = (
        "cryptography.hazmat.primitives.ciphers.algorithms",
    )

    severity = Severity.INFO

    status = "APPROVED"

    message = "ChaCha20 detected."

    recommendation = (
        "Review nonce management and authentication; "
        "prefer an authenticated construction where appropriate."
    )

    reference = "RFC 8439"