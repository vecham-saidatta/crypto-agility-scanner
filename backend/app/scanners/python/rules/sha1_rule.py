from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule


class SHA1Rule(BaseCryptoRule):
    """
    Detects SHA-1 usage.
    """

    algorithm = "SHA-1"

    function_name = "sha1"

    severity = "HIGH"

    message = "SHA-1 detected."

    recommendation = (
        "Replace SHA-1 with SHA-256 or SHA-3."
    )

    reference = "NIST SP 800-131A"