from app.cbom.cbom import CBOM
from app.cbom.component import CBOMComponent


def test_cbom_stores_components():
    components = [
        CBOMComponent(
            algorithm="RSA",
            file="app.py",
            line=51,
            properties={
                "key_size": 2048,
            },
        ),
        CBOMComponent(
            algorithm="AES",
            file="crypto.py",
            line=17,
            properties={},
        ),
    ]

    cbom = CBOM(
        components=components
    )

    assert cbom.components == components

def test_cbom_defaults_to_empty_components():
    cbom = CBOM()

    assert cbom.components == []