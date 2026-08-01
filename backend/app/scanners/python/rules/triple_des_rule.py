from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity


class TripleDESRule(BaseCryptoRule):

    algorithm = "TripleDES"
    
    function_name = "TripleDES"

    allowed_modules = (
        "cryptography.hazmat.primitives.ciphers.algorithms",
    )

    severity = Severity.HIGH

    status = "DEPRECATED"

    message = "Triple DES detected."

    recommendation = (
        "Plan migration from Triple DES to an approved "
        "modern authenticated encryption design."
    )

    reference = "NIST SP 800-131A"