from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule
from app.scanners.severity import Severity


class DESRule(BaseCryptoRule):

    algorithm = "DES"

    function_name = "DES"

    severity = Severity.HIGH
    
    status = "DEPRECATED"

    message = "DES detected."

    recommendation = (
        "Migrate DES usage to an approved modern "
        "authenticated encryption design."
    )

    reference = "NIST SP 800-131A"