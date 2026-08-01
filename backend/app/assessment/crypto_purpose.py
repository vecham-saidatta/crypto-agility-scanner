from enum import Enum


class CryptoPurpose(str, Enum):
    """
    Describes the security purpose for which
    a cryptographic primitive is being used.
    """

    DIGITAL_SIGNATURE = "DIGITAL_SIGNATURE"

    KEY_ESTABLISHMENT = "KEY_ESTABLISHMENT"

    ENCRYPTION = "ENCRYPTION"

    HASHING = "HASHING"

    UNKNOWN = "UNKNOWN"