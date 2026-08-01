import ast

from app.scanners.findings import Finding
from app.scanners.python.rules.base_crypto_rule import (
    BaseCryptoRule,
)


class ECDHRule(BaseCryptoRule):
    """
    Detects Elliptic Curve Diffie-Hellman
    key-agreement usage.
    """

    algorithm = "ECDH"

    severity = "INFO"

    status = "QUANTUM_VULNERABLE"

    message = "ECDH key-agreement usage detected."

    recommendation = (
        "Inventory this ECDH usage for "
        "post-quantum key-establishment "
        "migration planning."
    )

    reference = "NIST SP 800-56A Rev. 3"

    ECDH_FUNCTION = (
        "cryptography.hazmat.primitives."
        "asymmetric.ec.ECDH"
    )

    def check(
        self,
        node: ast.AST,
        file_path: str,
        imports: dict[
            str,
            list[tuple[int, str | None]],
        ],
    ) -> list[Finding]:

        if not isinstance(
            node,
            ast.Call,
        ):
            return []

        resolved_function = self._resolve_function(
            node.func,
            imports,
            node.lineno,
        )

        if (
            resolved_function
            != self.ECDH_FUNCTION
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
                metadata={
                    "operation": "key_agreement",
                },
            )
        ]