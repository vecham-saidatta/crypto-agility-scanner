from pathlib import Path

from app.services.scanner_service import ScannerService


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TEST_REPOSITORY = (
    PROJECT_ROOT
    / "backend"
    / "test_repository"
)


def test_scanner_service_generates_complete_report():

    service = ScannerService()

    report = service.scan(
        TEST_REPOSITORY
    )

    assert (
        report["summary"]["files_scanned"]
        == 2
    )

    assert (
        report["summary"]["total_findings"]
        == 17
    )

    assert (
        report["summary"]["security_findings_count"]
        == 5
    )

    assert (
        report["summary"]["quantum_vulnerable_count"]
        == 4
    )

    assert (
        report["summary"]["migration_required_count"]
        == 4
    )

    assert (
        report["risk"]["overall_risk"]
        == "HIGH"
    )

    assert (
        report["algorithm_inventory"]["MD5"]
        == 2
    )

    assert (
        report["algorithm_inventory"]["RSA"]
        == 1
    )

    assert (
        report["algorithm_inventory"]["ECDSA"]
        == 1
    )