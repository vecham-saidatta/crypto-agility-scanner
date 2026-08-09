from app.taxonomy.crypto_taxonomy import (
    CryptoAlgorithm,
    CryptoOperation,
    CryptoPurpose,
    FindingSeverity,
    CryptoStatus,
    normalize_algorithm,
    normalize_severity,
    normalize_status,
)


def test_algorithm_values_are_stable():

    assert CryptoAlgorithm.RSA == "RSA"

    assert (
        CryptoAlgorithm.RSA_SIGNATURE
        == "RSA-SIGNATURE"
    )

    assert (
        CryptoAlgorithm.RSA_ENCRYPTION
        == "RSA-ENCRYPTION"
    )

    assert CryptoAlgorithm.ECDSA == "ECDSA"

    assert CryptoAlgorithm.ECDH == "ECDH"


def test_hash_algorithm_values_are_stable():

    assert CryptoAlgorithm.MD5 == "MD5"

    assert CryptoAlgorithm.SHA1 == "SHA-1"

    assert (
        CryptoAlgorithm.SHA256
        == "SHA-256"
    )


def test_crypto_operation_values():

    assert (
        CryptoOperation.ENCRYPT
        == "ENCRYPT"
    )

    assert (
        CryptoOperation.DECRYPT
        == "DECRYPT"
    )

    assert CryptoOperation.SIGN == "SIGN"

    assert (
        CryptoOperation.KEY_AGREEMENT
        == "KEY_AGREEMENT"
    )


def test_crypto_purpose_values():

    assert (
        CryptoPurpose.DIGITAL_SIGNATURE
        == "DIGITAL_SIGNATURE"
    )

    assert (
        CryptoPurpose.KEY_ESTABLISHMENT
        == "KEY_ESTABLISHMENT"
    )

    assert (
        CryptoPurpose.UNKNOWN
        == "UNKNOWN"
    )


def test_finding_severity_values():

    assert (
        FindingSeverity.CRITICAL
        == "CRITICAL"
    )

    assert FindingSeverity.HIGH == "HIGH"

    assert FindingSeverity.INFO == "INFO"


def test_crypto_status_values():

    assert (
        CryptoStatus.APPROVED
        == "APPROVED"
    )

    assert (
        CryptoStatus.DEPRECATED
        == "DEPRECATED"
    )

    assert (
        CryptoStatus.QUANTUM_VULNERABLE
        == "QUANTUM_VULNERABLE"
    )

def test_normalizes_algorithm_aliases():

    assert (
        normalize_algorithm("SHA256")
        == "SHA-256"
    )

    assert (
        normalize_algorithm("sha-256")
        == "SHA-256"
    )

    assert (
        normalize_algorithm("3des")
        == "TripleDES"
    )

    assert (
        normalize_algorithm("rsa_signature")
        == "RSA-SIGNATURE"
    )

    assert (
        normalize_algorithm("RSA Encryption")
        == "RSA-ENCRYPTION"
    )


def test_normalizes_algorithm_enum():

    assert (
        normalize_algorithm(
            CryptoAlgorithm.ECDSA
        )
        == "ECDSA"
    )


def test_normalizes_severity():

    assert (
        normalize_severity("high")
        == "HIGH"
    )

    assert (
        normalize_severity(
            FindingSeverity.INFO
        )
        == "INFO"
    )


def test_normalizes_status():

    assert (
        normalize_status("approved")
        == "APPROVED"
    )

    assert (
        normalize_status(
            CryptoStatus.QUANTUM_VULNERABLE
        )
        == "QUANTUM_VULNERABLE"
    )