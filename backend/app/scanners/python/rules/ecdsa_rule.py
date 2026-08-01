import ast

from app.scanners.findings import Finding
from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule


class ECDSARule(BaseCryptoRule):
    """
    Detects ECDSA signature algorithm usage
    and extracts the configured hash algorithm.
    """

    algorithm = "ECDSA"

    severity = "INFO"

    status = "QUANTUM_VULNERABLE"

    message = "ECDSA signature usage detected."

    recommendation = (
        "Inventory this ECDSA usage for "
        "post-quantum signature migration planning."
    )

    reference = "NIST FIPS 186-5"

    ECDSA_FUNCTION = (
        "cryptography.hazmat.primitives."
        "asymmetric.ec.ECDSA"
    )

    HASH_PREFIX = (
        "cryptography.hazmat.primitives."
        "hashes."
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

        if not isinstance(node, ast.Call):
            return []

        resolved_function = self._resolve_function(
            node.func,
            imports,
            node.lineno,
        )

        if (
            resolved_function
            != self.ECDSA_FUNCTION
        ):
            return []

        hash_algorithm = (
            self._extract_hash_algorithm(
                node,
                imports,
            )
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
                    "hash_algorithm": (
                        hash_algorithm
                    ),
                },
            )
        ]

    def _extract_hash_algorithm(
        self,
        node: ast.Call,
        imports: dict[
            str,
            list[tuple[int, str | None]],
        ],
    ) -> str | None:

        if not node.args:
            return None

        hash_argument = node.args[0]

        if not isinstance(
            hash_argument,
            ast.Call,
        ):
            return None

        resolved_hash = self._resolve_function(
            hash_argument.func,
            imports,
            node.lineno,
        )

        if resolved_hash is None:
            return None

        if not resolved_hash.startswith(
            self.HASH_PREFIX
        ):
            return None

        hash_name = resolved_hash.removeprefix(
            self.HASH_PREFIX
        )

        return self._normalize_hash_name(
            hash_name
        )

    def _normalize_hash_name(
        self,
        hash_name: str,
    ) -> str:

        names = {
            "SHA1": "SHA-1",
            "SHA224": "SHA-224",
            "SHA256": "SHA-256",
            "SHA384": "SHA-384",
            "SHA512": "SHA-512",
        }

        return names.get(
            hash_name,
            hash_name,
        )