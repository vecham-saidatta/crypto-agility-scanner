from enum import StrEnum


class CryptoAlgorithm(StrEnum):
    """
    Canonical algorithm identifiers used throughout
    the crypto-agility scanner.
    """

    MD5 = "MD5"

    SHA1 = "SHA-1"
    SHA224 = "SHA-224"
    SHA256 = "SHA-256"
    SHA384 = "SHA-384"
    SHA512 = "SHA-512"

    AES = "AES"
    TRIPLE_DES = "TripleDES"
    RC4 = "RC4"
    CHACHA20 = "ChaCha20"

    RSA = "RSA"
    RSA_SIGNATURE = "RSA-SIGNATURE"
    RSA_ENCRYPTION = "RSA-ENCRYPTION"

    ECC = "ECC"
    ECDSA = "ECDSA"
    ECDH = "ECDH"


class CryptoOperation(StrEnum):
    """
    Canonical cryptographic operations.
    """

    HASH = "HASH"

    ENCRYPT = "ENCRYPT"
    DECRYPT = "DECRYPT"

    SIGN = "SIGN"
    VERIFY = "VERIFY"

    KEY_GENERATION = "KEY_GENERATION"
    KEY_AGREEMENT = "KEY_AGREEMENT"


class CryptoPurpose(StrEnum):
    """
    High-level purpose of a cryptographic usage.
    """

    HASHING = "HASHING"

    DATA_ENCRYPTION = "DATA_ENCRYPTION"

    DIGITAL_SIGNATURE = "DIGITAL_SIGNATURE"

    KEY_ESTABLISHMENT = "KEY_ESTABLISHMENT"

    UNKNOWN = "UNKNOWN"


class FindingSeverity(StrEnum):
    """
    Canonical scanner severity values.
    """

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class CryptoStatus(StrEnum):
    """
    Canonical crypto status values.
    """

    APPROVED = "APPROVED"

    DEPRECATED = "DEPRECATED"

    DISALLOWED = "DISALLOWED"

    QUANTUM_VULNERABLE = (
        "QUANTUM_VULNERABLE"
    )

    REVIEW_REQUIRED = "REVIEW_REQUIRED"

    UNKNOWN = "UNKNOWN"

def normalize_algorithm(
    value: str | CryptoAlgorithm,
) -> str:
    """
    Normalize an algorithm identifier to its
    canonical scanner representation.
    """

    if isinstance(value, CryptoAlgorithm):
        return value.value

    normalized = value.strip().upper()

    aliases = {
        "SHA1": CryptoAlgorithm.SHA1.value,
        "SHA-1": CryptoAlgorithm.SHA1.value,

        "SHA224": CryptoAlgorithm.SHA224.value,
        "SHA-224": CryptoAlgorithm.SHA224.value,

        "SHA256": CryptoAlgorithm.SHA256.value,
        "SHA-256": CryptoAlgorithm.SHA256.value,

        "SHA384": CryptoAlgorithm.SHA384.value,
        "SHA-384": CryptoAlgorithm.SHA384.value,

        "SHA512": CryptoAlgorithm.SHA512.value,
        "SHA-512": CryptoAlgorithm.SHA512.value,

        "3DES": CryptoAlgorithm.TRIPLE_DES.value,
        "TRIPLEDES": CryptoAlgorithm.TRIPLE_DES.value,

        "CHACHA20": CryptoAlgorithm.CHACHA20.value,

        "RSA_SIGNATURE": (
            CryptoAlgorithm.RSA_SIGNATURE.value
        ),
        "RSA SIGNATURE": (
            CryptoAlgorithm.RSA_SIGNATURE.value
        ),
        "RSA-SIGNATURE": (
            CryptoAlgorithm.RSA_SIGNATURE.value
        ),

        "RSA_ENCRYPTION": (
            CryptoAlgorithm.RSA_ENCRYPTION.value
        ),
        "RSA ENCRYPTION": (
            CryptoAlgorithm.RSA_ENCRYPTION.value
        ),
        "RSA-ENCRYPTION": (
            CryptoAlgorithm.RSA_ENCRYPTION.value
        ),
    }

    if normalized in aliases:
        return aliases[normalized]

    for algorithm in CryptoAlgorithm:
        if normalized == algorithm.value.upper():
            return algorithm.value

    return value.strip()

def normalize_severity(
    value: str | FindingSeverity,
) -> str:
    """
    Normalize finding severity.
    """

    if isinstance(value, FindingSeverity):
        return value.value

    normalized = value.strip().upper()

    try:
        return FindingSeverity(
            normalized
        ).value

    except ValueError:
        return normalized


def normalize_status(
    value: str | CryptoStatus,
) -> str:
    """
    Normalize cryptographic status.
    """

    if isinstance(value, CryptoStatus):
        return value.value

    normalized = value.strip().upper()

    try:
        return CryptoStatus(
            normalized
        ).value

    except ValueError:
        return normalized