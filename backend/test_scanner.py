import argparse
import json
import sys
from pathlib import Path

from app.services.scanner_service import ScannerService
from app.services.workspace_service import (
    WorkspaceService,
)
from app.services.repository_resolver import (
    RepositoryResolver,
)

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
    print("=" * 60)
    print("Findings")
    print("=" * 60)

    important_findings = [
        finding
        for finding in report["findings"]
        if finding["severity"] in {"HIGH", "CRITICAL"}
    ]

    if not important_findings:
        print("No HIGH or CRITICAL findings.")
    else:
        for finding in important_findings:
            print(
                f'{finding["severity"]}  '
                f'{finding["algorithm"]}'
            )
            print(
                f'      {finding["file"]}:'
                f'{finding["line"]}'
            )
            print(
                f'      {finding["message"]}'
            )
            print(
                f'      Recommendation: '
                f'{finding["recommendation"]}'
            )
            print()
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
    parser.add_argument(
        "--output",
        type=Path,
        help=(
            "Write the JSON report to a file."
        ),
    )

    args = parser.parse_args()

    try:
        resolved_repository = (
            RepositoryResolver.resolve_with_workspace(
                args.repository
            )
        )

        repository_path = (
            resolved_repository.repository_path
        )

        workspace_path = (
            resolved_repository.workspace_path
        )

    except Exception as exc:
        print(
            f"Error: {exc}",
            file=sys.stderr,
        )
        return 2


    print("=" * 60)
    print("Crypto Agility Scanner")
    print("=" * 60)

    print(
        f"Repository: {repository_path}"
    )

    service = ScannerService()

    try:
        report = service.scan(
            repository_path
        )

        if args.format == "json":

            output = json.dumps(
                report,
                indent=4,
            )

            if args.output is not None:

                args.output.write_text(
                    output,
                    encoding="utf-8",
                )

                print(
                    f"Report written to: "
                    f"{args.output}"
                )

            else:
                print(output)

            return get_exit_code(
                report
            )

        print_terminal_report(
            report
        )

        return get_exit_code(
            report
        )

    finally:
        if workspace_path is not None:
            WorkspaceService().cleanup_scan_workspace(
                workspace_path
            )

if __name__ == "__main__":
    sys.exit(
        main()
    )