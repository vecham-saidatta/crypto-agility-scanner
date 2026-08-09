import json
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch


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
