from app.scanners.python.rules.base_crypto_rule import (
    BaseCryptoRule,
)
from app.taxonomy.crypto_taxonomy import (
    CryptoAlgorithm,
    FindingSeverity,
    CryptoStatus,
)


class MD5Rule(BaseCryptoRule):
    """
    Detects MD5 usage.
    """

    algorithm = CryptoAlgorithm.MD5

    function_name = "md5"

    allowed_modules = ("hashlib",)

    severity = FindingSeverity.HIGH

    status = CryptoStatus.DEPRECATED

    message = "MD5 detected."

    recommendation = (
        "Replace MD5 with SHA-256 or SHA-3."
    )

    reference = "NIST SP 800-131A"