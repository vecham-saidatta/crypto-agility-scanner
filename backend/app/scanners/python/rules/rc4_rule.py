from app.scanners.python.rules.base_crypto_rule import (
    BaseCryptoRule,
)
from app.taxonomy.crypto_taxonomy import (
    CryptoAlgorithm,
    FindingSeverity,
    CryptoStatus,
)


class RC4Rule(BaseCryptoRule):
    """
    Detects RC4/ARC4 usage.
    """

    algorithm = CryptoAlgorithm.RC4

    function_name = "ARC4"

    allowed_modules = (
        "cryptography.hazmat.primitives.ciphers.algorithms",
    )

    severity = FindingSeverity.HIGH

    status = CryptoStatus.DEPRECATED

    message = "RC4/ARC4 detected."

    recommendation = (
        "Replace RC4 with an approved modern "
        "authenticated encryption design."
    )

    reference = "RFC 7465"