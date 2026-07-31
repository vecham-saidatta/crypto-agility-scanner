from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule


class MD5Rule(BaseCryptoRule):
    """
    Detects MD5 usage.
    """

    algorithm = "MD5"

    function_name = "md5"

    severity = "HIGH"

    message = "MD5 detected."

    recommendation = (
        "Replace MD5 with SHA-256 or SHA-3."
    )

    reference = "NIST SP 800-131A"