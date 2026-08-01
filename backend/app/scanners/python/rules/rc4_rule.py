from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity


class RC4Rule(BaseCryptoRule):

    algorithm = "RC4"

    function_name = "ARC4"

    allowed_modules = (
        "cryptography.hazmat.primitives.ciphers.algorithms",
    )

    severity = Severity.HIGH

    status = "DEPRECATED"

    message = "RC4/ARC4 detected."

    recommendation = (
        "Replace RC4 with an approved modern "
        "authenticated encryption design."
    )

    reference = "RFC 7465"