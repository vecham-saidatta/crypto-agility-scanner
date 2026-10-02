import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch
from backend.test_scanner import main


PROJECT_ROOT = Path(__file__).resolve().parents[2]

SCANNER = (
    PROJECT_ROOT
    / "backend"
    / "test_scanner.py"
)

TEST_REPOSITORY = (
    PROJECT_ROOT
    / "backend"
    / "test_repository"
)


def run_scanner(*args):
    result = subprocess.run(
        [
            sys.executable,
            str(SCANNER),
            *args,
        ],
        cwd=PROJECT_ROOT,
        env={
            **os.environ,
            "PYTHONPATH": str(
                PROJECT_ROOT / "backend"
            ),
        },
        capture_output=True,
        text=True,
    )

    return result


def test_terminal_scan_returns_high_risk_exit_code():

    result = run_scanner(
        str(TEST_REPOSITORY)
    )

    assert result.returncode == 1

    assert (
        "Overall risk: HIGH"
        in result.stdout
    )


def test_json_scan_returns_high_risk_exit_code():

    result = run_scanner(
        str(TEST_REPOSITORY),
        "--format",
        "json",
    )

    assert result.returncode == 1

    json_start = result.stdout.find("{")

    assert json_start != -1

    report = json.loads(
        result.stdout[json_start:]
    )

    assert (
        report["risk"]["overall_risk"]
        == "HIGH"
    )


def test_invalid_repository_returns_error_code():

    result = run_scanner(
        "does_not_exist"
    )

    assert result.returncode == 2

    assert (
        "Repository path does not exist"
        in result.stderr
    )


def test_invalid_format_is_rejected():

    result = run_scanner(
        str(TEST_REPOSITORY),
        "--format",
        "xml",
    )

    assert result.returncode == 2

    assert (
        "invalid choice"
        in result.stderr
    )

def test_json_output_file_is_created(
    tmp_path,
):
    output_file = (
        tmp_path / "report.json"
    )

    result = run_scanner(
        str(TEST_REPOSITORY),
        "--format",
        "json",
        "--output",
        str(output_file),
    )

    assert result.returncode == 1

    assert output_file.exists()

    report = json.loads(
        output_file.read_text(
            encoding="utf-8"
        )
    )

    assert (
        report["risk"]["overall_risk"]
        == "HIGH"
    )


def test_output_file_does_not_change_exit_code(
    tmp_path,
):
    output_file = (
        tmp_path / "report.json"
    )

    result = run_scanner(
        str(TEST_REPOSITORY),
        "--format",
        "json",
        "--output",
        str(output_file),
    )

    assert result.returncode == 1

def test_remote_scan_cleans_up_workspace(
    tmp_path,
    monkeypatch,
):
    workspace_path = (
        tmp_path / "scan-workspace"
    )

    repository_path = (
        workspace_path / "repository"
    )

    workspace_path.mkdir()
    repository_path.mkdir()

    class FakeResolvedRepository:
        pass

    resolved = FakeResolvedRepository()
    resolved.repository_path = repository_path
    resolved.workspace_path = workspace_path

    cleanup_calls = []

    class FakeWorkspaceService:
        def cleanup_scan_workspace(
            self,
            path,
        ):
            cleanup_calls.append(path)

    fake_report = {
        "summary": {
            "files_scanned": 0,
            "total_findings": 0,
            "crypto_inventory_count": 0,
            "security_findings_count": 0,
            "approved_crypto_count": 0,
            "quantum_vulnerable_count": 0,
            "migration_required_count": 0,
        },
        "risk": {
            "overall_risk": "LOW",
            "severity_count": {},
        },
        "algorithm_inventory": {},
    }

    monkeypatch.setattr(
        "backend.test_scanner.RepositoryResolver.resolve_with_workspace",
        lambda repository: resolved,
    )

    monkeypatch.setattr(
        "backend.test_scanner.WorkspaceService",
        FakeWorkspaceService,
    )

    monkeypatch.setattr(
        "backend.test_scanner.ScannerService.scan",
        lambda self, path: fake_report,
    )

    monkeypatch.setattr(
        "sys.argv",
        [
            "test_scanner.py",
            "https://github.com/example/repository",
        ],
    )

    result = main()

    assert result == 0

    assert cleanup_calls == [
        workspace_path
    ]