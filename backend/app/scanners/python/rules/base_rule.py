from abc import ABC, abstractmethod
import ast

from app.scanners.findings import Finding


class BaseRule(ABC):
    """
    Base interface for Python scanner rules.
    """

    @abstractmethod
    def check(
        self,
        node: ast.AST,
        file_path: str,
        imports: dict[
            str,
            list[tuple[int, str | None]],
        ],
    ) -> list[Finding]:
        """
        Check an AST node and return security findings.
        """
        pass