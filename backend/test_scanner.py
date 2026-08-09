import argparse
import json
import sys
from pathlib import Path

from app.services.scanner_service import ScannerService


def print_terminal_report(report: dict) -> None:
    summary = report["summary"]
    risk = report["risk"]

    print()
    print("=" * 60)
    print("Security Summary")
    print("=" * 60)

    print(
        f"Files scanned: "
        f"{summary['files_scanned']}"
    )

    print(
        f"Total findings: "
        f"{summary['total_findings']}"
    )

    print(
        f"Crypto inventory: "
        f"{summary['crypto_inventory_count']}"
    )

    print(
        f"Security findings: "
        f"{summary['security_findings_count']}"
    )

    print(
        f"Approved crypto: "
        f"{summary['approved_crypto_count']}"
    )

    print(
        f"Quantum vulnerable: "
        f"{summary['quantum_vulnerable_count']}"
    )

    print(
        f"Migration required: "
        f"{summary['migration_required_count']}"
    )

    print(
        f"Overall risk: "
        f"{risk['overall_risk']}"
    )

    print()
    print("Severity")
    print("-" * 60)

    for severity, count in risk[
        "severity_count"
    ].items():
        print(
            f"{severity}: {count}"
        )

    print()
    print("Algorithm Inventory")
    print("-" * 60)

    for algorithm, count in report[
        "algorithm_inventory"
    ].items():
        print(
            f"{algorithm}: {count}"
        )

def get_exit_code(
    report: dict,
) -> int:
    """
    Determine the CLI exit code from the
    security report.
    """

    overall_risk = report[
        "risk"
    ][
        "overall_risk"
    ]

    if overall_risk in {
        "HIGH",
        "CRITICAL",
    }:
        return 1

    return 0

def main():
    parser = argparse.ArgumentParser(
        description="Crypto Agility Scanner"
    )

    parser.add_argument(
        "repository",
        help="Path to the repository to scan.",
    )

    parser.add_argument(
        "--format",
        choices=[
            "terminal",
            "json",
        ],
        default="terminal",
        help=(
            "Output format. "
            "Default: terminal."
        ),
    )

    args = parser.parse_args()

    repository_path = Path(
        args.repository
    )

    if not repository_path.exists():
        parser.error(
            "Repository path does not exist: "
            f"{repository_path}"
        )

    if not repository_path.is_dir():
        parser.error(
            "Repository path is not a directory: "
            f"{repository_path}"
        )

    print("=" * 60)
    print("Crypto Agility Scanner")
    print("=" * 60)

    print(
        f"Repository: {repository_path}"
    )

    service = ScannerService()

    report = service.scan(
        repository_path
    )

    if args.format == "json":
        print(
            json.dumps(
                report,
                indent=4,
            )
        )

        return get_exit_code(
            report
        )

    print_terminal_report(
        report
    )

    return get_exit_code(
        report
    )

if __name__ == "__main__":
    sys.exit(
        main()
    )