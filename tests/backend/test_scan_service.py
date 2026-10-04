from pathlib import Path

from app.services.scan_service import ScanService


PROJECT_ROOT = Path(__file__).resolve().parents[2]

TEST_REPOSITORY_URL = (
    "https://github.com/example/test-repository"
)


def test_scan_service_returns_scan_report(monkeypatch):

    expected_report = {
        "summary": {
            "files_scanned": 2,
        },
        "risk": {
            "overall_risk": "HIGH",
        },
        "cbom": {
            "components": [],
        },
    }

    class FakePreparedRepository:
        repository_path = PROJECT_ROOT / "backend" / "test_repository"
        workspace_path = PROJECT_ROOT / "workspace" / "test-scan"

    def fake_prepare_repository(repository_url):
        assert repository_url == TEST_REPOSITORY_URL
        return FakePreparedRepository()

    def fake_scan(repository_path):
        assert (
            repository_path
            == FakePreparedRepository.repository_path
        )
        return expected_report

    def fake_cleanup(
        self,
        workspace_path,
    ):
        assert (
            workspace_path
            == FakePreparedRepository.workspace_path
        )

    monkeypatch.setattr(
        "app.services.scan_service.prepare_repository_with_workspace",
        fake_prepare_repository,
    )

    monkeypatch.setattr(
        "app.services.scan_service.ScannerService.scan",
        staticmethod(fake_scan),
    )

    monkeypatch.setattr(
        "app.services.scan_service.WorkspaceService.cleanup_scan_workspace",
        fake_cleanup,
    )

    service = ScanService()

    report = service.scan(
        TEST_REPOSITORY_URL
    )

    assert report == expected_report
def test_scan_service_cleans_up_when_scan_fails(monkeypatch):

    class FakePreparedRepository:
        repository_path = PROJECT_ROOT / "backend" / "test_repository"
        workspace_path = PROJECT_ROOT / "workspace" / "test-scan"

    def fake_prepare_repository(repository_url):
        return FakePreparedRepository()

    def fake_scan(repository_path):
        raise RuntimeError("Scan failed")

    cleanup_called = False

    def fake_cleanup(
        self,
        workspace_path,
    ):
        nonlocal cleanup_called

        assert (
            workspace_path
            == FakePreparedRepository.workspace_path
        )

        cleanup_called = True

    monkeypatch.setattr(
        "app.services.scan_service.prepare_repository_with_workspace",
        fake_prepare_repository,
    )

    monkeypatch.setattr(
        "app.services.scan_service.ScannerService.scan",
        staticmethod(fake_scan),
    )

    monkeypatch.setattr(
        "app.services.scan_service.WorkspaceService.cleanup_scan_workspace",
        fake_cleanup,
    )

    service = ScanService()

    try:
        service.scan(
            TEST_REPOSITORY_URL
        )
    except RuntimeError:
        pass

    assert cleanup_called is True
