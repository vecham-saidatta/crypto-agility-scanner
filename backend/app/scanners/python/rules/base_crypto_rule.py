import ast

from app.scanners.findings import Finding
from app.scanners.python.rules.base_rule import BaseRule


class BaseCryptoRule(BaseRule):
    """
    Base class for cryptographic detection rules.
    """

    algorithm: str
    function_name: str
    allowed_modules: tuple[str, ...] = ()
    severity: str
    status: str
    message: str
    recommendation: str
    reference: str

    def check(
        self,
        node: ast.AST,
        file_path: str,
        imports: dict[
            str,
            list[tuple[int, str | None]],
        ],
    ) -> list[Finding]:

        if not isinstance(node, ast.Call):
            return []

        resolved_function = self._resolve_function(
            node.func,
            imports,
            node.lineno,
        )
        if resolved_function is None:
            return []

        if resolved_function.split(".")[-1] != self.function_name:
            return []
        if self.allowed_modules:

            module_path = resolved_function.rsplit(".", 1)[0]

            if not any(
                module_path == allowed_module
                or module_path.startswith(
                    f"{allowed_module}."
                )
                for allowed_module in self.allowed_modules
            ):
                return []
        return [
            Finding(
                algorithm=self.algorithm,
                file_path=file_path,
                line_number=node.lineno,
                severity=self.severity,
                status=self.status,
                message=self.message,
                recommendation=self.recommendation,
                reference=self.reference,
            )
        ]

    def _resolve_function(
        self,
        function: ast.AST,
        imports: dict[
            str,
            list[tuple[int, str | None]],
        ],
        line_number: int,
    ) -> str | None:

        # Example:
        #
        # from hashlib import md5
        # md5(...)
        #
        # Look at the history of "md5" and determine
        # what it meant at this line.
        if isinstance(function, ast.Name):

            history = imports.get(
                function.id,
                [],
            )

            resolved = None

            for symbol_line, symbol_path in history:

                if symbol_line > line_number:
                    break

                resolved = symbol_path

            return resolved

        # Examples:
        #
        # hashlib.md5(...)
        # algorithms.AES(...)
        # hl.sha256(...)
        if isinstance(function, ast.Attribute):

            resolved_parent = self._resolve_function(
                function.value,
                imports,
                line_number,
            )

            if resolved_parent is None:
                return None

            return f"{resolved_parent}.{function.attr}"

        return None