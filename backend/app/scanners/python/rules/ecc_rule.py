import ast

from app.scanners.findings import Finding
from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule


class ECCRule(BaseCryptoRule):
    """
    Detects elliptic-curve private-key generation
    and extracts the selected curve.
    """

    algorithm = "ECC"

    function_name = "generate_private_key"

    allowed_modules = (
        "cryptography.hazmat.primitives.asymmetric.ec",
    )

    severity = "INFO"

    status = "QUANTUM_VULNERABLE"

    message = "Elliptic-curve key generation detected."

    recommendation = (
        "Inventory this elliptic-curve usage for "
        "post-quantum migration planning."
    )

    reference = "NIST SP 800-186"

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

        expected_function = (
            "cryptography.hazmat.primitives."
            "asymmetric.ec.generate_private_key"
        )

        if resolved_function != expected_function:
            return []

        curve = self._extract_curve(
            node,
            imports,
        )

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
                metadata={
                    "curve": curve,
                },
            )
        ]

    def _extract_curve(
        self,
        node: ast.Call,
        imports: dict[
            str,
            list[tuple[int, str | None]],
        ],
    ) -> str | None:

        if not node.args:
            return None

        curve_argument = node.args[0]

        if not isinstance(
            curve_argument,
            ast.Call,
        ):
            return None

        resolved_curve = self._resolve_function(
            curve_argument.func,
            imports,
            node.lineno,
        )

        if resolved_curve is None:
            return None

        curve_prefix = (
            "cryptography.hazmat.primitives."
            "asymmetric.ec."
        )

        if not resolved_curve.startswith(
            curve_prefix
        ):
            return None

        return resolved_curve.removeprefix(
            curve_prefix
        )