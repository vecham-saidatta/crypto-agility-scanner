from app.cbom.component import CBOMComponent
from app.cbom.converter import CBOMConverter
from app.scanners.findings import Finding


def test_converter_creates_component_from_finding():
    finding = Finding(
        algorithm="RSA",
        file_path="app.py",
        line_number=51,
        severity="INFO",
        status="QUANTUM_VULNERABLE",
        message="RSA key generation detected.",
        recommendation="Inventory this RSA usage.",
        reference="NIST FIPS 186-5",
        metadata={
            "key_size": 2048,
            "public_exponent": 65537,
        },
    )

    converter = CBOMConverter()

    component = converter.from_finding(
        finding
    )

    assert component == CBOMComponent(
        algorithm="RSA",
        file="app.py",
        line=51,
        properties={
            "key_size": 2048,
            "public_exponent": 65537,
        },
    )

def test_converter_handles_finding_without_metadata():
    finding = Finding(
        algorithm="AES",
        file_path="crypto.py",
        line_number=17,
        severity="INFO",
        status="APPROVED",
        message="AES usage detected.",
        recommendation="No migration required.",
        reference="",
    )

    converter = CBOMConverter()

    component = converter.from_finding(
        finding
    )

    assert component == CBOMComponent(
        algorithm="AES",
        file="crypto.py",
        line=17,
        properties={},
    )

def test_converter_copies_metadata():
    finding = Finding(
        algorithm="RSA",
        file_path="app.py",
        line_number=51,
        severity="INFO",
        status="QUANTUM_VULNERABLE",
        message="RSA key generation detected.",
        recommendation="Inventory this RSA usage.",
        reference="NIST FIPS 186-5",
        metadata={
            "key_size": 2048,
        },
    )

    converter = CBOMConverter()

    component = converter.from_finding(
        finding
    )

    component.properties["key_size"] = 4096

    assert finding.metadata["key_size"] == 2048

def test_converter_creates_components_from_multiple_findings():
    findings = [
        Finding(
            algorithm="RSA",
            file_path="app.py",
            line_number=51,
            severity="INFO",
            status="QUANTUM_VULNERABLE",
            message="RSA key generation detected.",
            recommendation="Inventory this RSA usage.",
            reference="NIST FIPS 186-5",
            metadata={
                "key_size": 2048,
            },
        ),
        Finding(
            algorithm="AES",
            file_path="crypto.py",
            line_number=17,
            severity="INFO",
            status="APPROVED",
            message="AES usage detected.",
            recommendation="No migration required.",
            reference="",
        ),
    ]

    converter = CBOMConverter()

    components = converter.from_findings(
        findings
    )

    assert components == [
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

def test_converter_creates_cbom_from_findings():
    findings = [
        Finding(
            algorithm="RSA",
            file_path="app.py",
            line_number=51,
            severity="INFO",
            status="QUANTUM_VULNERABLE",
            message="RSA key generation detected.",
            recommendation="Inventory this RSA usage.",
            reference="NIST FIPS 186-5",
            metadata={
                "key_size": 2048,
            },
        ),
        Finding(
            algorithm="AES",
            file_path="crypto.py",
            line_number=17,
            severity="INFO",
            status="APPROVED",
            message="AES usage detected.",
            recommendation="No migration required.",
            reference="",
        ),
    ]

    converter = CBOMConverter()

    cbom = converter.convert(
        findings
    )

    assert cbom.components == [
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