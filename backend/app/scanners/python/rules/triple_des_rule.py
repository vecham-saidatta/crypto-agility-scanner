from app.scanners.python.rules.base_crypto_rule import (
    BaseCryptoRule,
)
from app.taxonomy.crypto_taxonomy import (
    CryptoAlgorithm,
    FindingSeverity,
    CryptoStatus,
)


class TripleDESRule(BaseCryptoRule):
    """
    Detects Triple DES usage.
    """

    algorithm = CryptoAlgorithm.TRIPLE_DES

    function_name = "TripleDES"

    allowed_modules = (
        "cryptography.hazmat.primitives.ciphers.algorithms",
    )

    severity = FindingSeverity.HIGH

    status = CryptoStatus.DEPRECATED

    message = "Triple DES detected."

    recommendation = (
        "Plan migration from Triple DES to an approved "
        "modern authenticated encryption design."
    )

    reference = "NIST SP 800-131A"