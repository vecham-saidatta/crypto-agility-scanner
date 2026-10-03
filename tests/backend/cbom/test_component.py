from app.cbom.component import CBOMComponent


def test_cbom_component_stores_crypto_inventory():
    component = CBOMComponent(
        algorithm="RSA",
        file="app.py",
        line=51,
        properties={
            "key_size": 2048,
            "public_exponent": 65537,
        },
    )

    assert component.algorithm == "RSA"
    assert component.file == "app.py"
    assert component.line == 51
    assert component.properties == {
        "key_size": 2048,
        "public_exponent": 65537,
    }
