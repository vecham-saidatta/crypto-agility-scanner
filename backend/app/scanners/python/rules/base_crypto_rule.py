import ast
from abc import abstractmethod

from app.scanners.findings import Finding
from app.scanners.python.rules.base_rule import BaseRule


class BaseCryptoRule(BaseRule):
    """
    Base class for cryptographic function detection rules.
    """

    algorithm: str
    function_name: str
    severity: str
    message: str
    recommendation: str
    reference: str

    def check(
        self,
        node: ast.AST,
        file_path: str,
    ) -> list[Finding]:

        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == self.function_name
        ):
            return [
                Finding(
                    algorithm=self.algorithm,
                    file_path=file_path,
                    line_number=node.lineno,
                    severity=self.severity,
                    message=self.message,
                    recommendation=self.recommendation,
                    reference=self.reference,
                )
            ]

        return []