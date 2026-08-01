from app.assessment.crypto_purpose import (
    CryptoPurpose,
)


def test_digital_signature_purpose():

    assert (
        CryptoPurpose.DIGITAL_SIGNATURE.value
        == "DIGITAL_SIGNATURE"
    )


def test_key_establishment_purpose():

    assert (
        CryptoPurpose.KEY_ESTABLISHMENT.value
        == "KEY_ESTABLISHMENT"
    )


def test_unknown_purpose():

    assert (
        CryptoPurpose.UNKNOWN.value
        == "UNKNOWN"
    )