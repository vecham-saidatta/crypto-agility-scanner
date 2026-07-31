from abc import ABC, abstractmethod
import ast

from app.scanners.findings import Finding


class BaseRule(ABC):
    """
    Base class for Python detection rules.
    """

    @abstractmethod
    def check(
        self,
        node: ast.AST,
        file_path: str,
    ) -> list[Finding]:
        pass