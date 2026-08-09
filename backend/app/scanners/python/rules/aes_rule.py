from app.scanners.python.rules.base_crypto_rule import (
    BaseCryptoRule,
)
from app.taxonomy.crypto_taxonomy import (
    CryptoAlgorithm,
    FindingSeverity,
    CryptoStatus,
)


class AESRule(BaseCryptoRule):
    """
    Detects AES usage.
    """

    algorithm = CryptoAlgorithm.AES

    function_name = "AES"

    allowed_modules = (
        "cryptography.hazmat.primitives.ciphers.algorithms",
    )

    severity = FindingSeverity.INFO

    status = CryptoStatus.APPROVED

    message = "AES detected."

    recommendation = (
        "Review key size, cipher mode, nonce/IV handling, "
        "and authentication configuration."
    )

    reference = "NIST FIPS 197"