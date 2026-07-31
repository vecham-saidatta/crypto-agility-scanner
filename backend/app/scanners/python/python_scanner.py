import ast
from pathlib import Path

from app.scanners.base_scanner import BaseScanner
from app.scanners.findings import Finding
from app.scanners.python.rules.rule_registry import RuleRegistry


class PythonScanner(BaseScanner):
    """
    Scanner responsible for analyzing Python source code.
    """

    def scan(
        self,
        files: list[Path],
    ) -> list[Finding]:

        findings: list[Finding] = []

        rules = RuleRegistry.get_rules()

        for file in files:

            try:
                source = file.read_text(
                    encoding="utf-8"
                )

                tree = ast.parse(source)

            except Exception:
                continue

            for node in ast.walk(tree):

                for rule in rules:

                    findings.extend(
                        rule.check(
                            node=node,
                            file_path=str(file),
                        )
                    )

        return findings