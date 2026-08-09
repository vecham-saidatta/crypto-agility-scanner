import ast

from app.scanners.findings import Finding
from app.scanners.python.rules.base_crypto_rule import (
    BaseCryptoRule,
)
from app.taxonomy.crypto_taxonomy import (
    CryptoAlgorithm,
    CryptoOperation,
    FindingSeverity,
    CryptoStatus,
)


class RSASignatureRule(BaseCryptoRule):
    """
    Detects RSA digital-signature operations.

    Initial implementation detects .sign()
    calls and requires RSA-specific padding
    evidence to avoid matching unrelated
    sign methods.
    """

    algorithm = CryptoAlgorithm.RSA_SIGNATURE

    severity = FindingSeverity.INFO

    status = CryptoStatus.QUANTUM_VULNERABLE

    message = "RSA digital-signature usage detected."

    recommendation = (
        "Inventory this RSA signature usage for "
        "post-quantum digital-signature migration."
    )

    reference = "NIST FIPS 186-5"

    RSA_PSS = (
        "cryptography.hazmat.primitives."
        "asymmetric.padding.PSS"
    )

    RSA_PKCS1V15 = (
        "cryptography.hazmat.primitives."
        "asymmetric.padding.PKCS1v15"
    )

    HASH_ALGORITHMS = {
        (
            "cryptography.hazmat.primitives."
            "hashes.SHA1"
        ): CryptoAlgorithm.SHA1.value,

        (
            "cryptography.hazmat.primitives."
            "hashes.SHA224"
        ): CryptoAlgorithm.SHA224.value,

        (
            "cryptography.hazmat.primitives."
            "hashes.SHA256"
        ): CryptoAlgorithm.SHA256.value,

        (
            "cryptography.hazmat.primitives."
            "hashes.SHA384"
        ): CryptoAlgorithm.SHA384.value,

        (
            "cryptography.hazmat.primitives."
            "hashes.SHA512"
        ): CryptoAlgorithm.SHA512.value,
    }

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

        if not isinstance(
            node.func,
            ast.Attribute,
        ):
            return []

        if node.func.attr != "sign":
            return []

        padding_name = self._extract_padding(
            node,
            imports,
        )

        # A random object.sign() must not be
        # classified as RSA.
        if padding_name is None:
            return []

        hash_algorithm = self._extract_hash(
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
                    "operation": CryptoOperation.SIGN.value,
                    "padding": padding_name,
                    "hash_algorithm": hash_algorithm,
                },
            )
        ]

    def _extract_padding(
        self,
        node: ast.Call,
        imports,
    ) -> str | None:

        for argument in node.args:

            if not isinstance(
                argument,
                ast.Call,
            ):
                continue

            resolved = self._resolve_function(
                argument.func,
                imports,
                argument.lineno,
            )

            if resolved == self.RSA_PSS:
                return "PSS"

            if resolved == self.RSA_PKCS1V15:
                return "PKCS1v15"

        return None

    def _extract_hash(
        self,
        node: ast.Call,
        imports,
    ) -> str | None:

        for argument in node.args:

            if not isinstance(
                argument,
                ast.Call,
            ):
                continue

            resolved = self._resolve_function(
                argument.func,
                imports,
                argument.lineno,
            )

            hash_name = (
                self.HASH_ALGORITHMS.get(
                    resolved
                )
            )

            if hash_name is not None:
                return hash_name

        return None