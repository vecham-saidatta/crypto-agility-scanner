from app.scanners.python.rules.base_crypto_rule import (
    BaseCryptoRule,
)
from app.taxonomy.crypto_taxonomy import (
    CryptoAlgorithm,
    FindingSeverity,
    CryptoStatus,
)


class ChaCha20Rule(BaseCryptoRule):
    """
    Detects ChaCha20 usage.
    """

    algorithm = CryptoAlgorithm.CHACHA20

    function_name = "ChaCha20"

    allowed_modules = (
        "cryptography.hazmat.primitives.ciphers.algorithms",
    )

    severity = FindingSeverity.INFO

    status = CryptoStatus.APPROVED

    message = "ChaCha20 detected."

    recommendation = (
        "Review nonce management and authentication; "
        "prefer an authenticated construction where appropriate."
    )

    reference = "RFC 8439"