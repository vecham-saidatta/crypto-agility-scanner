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


class RSAEncryptionRule(BaseCryptoRule):
    """
    Detects RSA encryption and decryption usage.
    """

    algorithm = CryptoAlgorithm.RSA_ENCRYPTION

    severity = FindingSeverity.INFO

    status = CryptoStatus.QUANTUM_VULNERABLE

    message = (
        "RSA encryption/decryption usage detected."
    )

    recommendation = (
        "Inventory this RSA encryption usage for "
        "post-quantum key-establishment migration."
    )

    reference = "NIST SP 800-56B Rev. 2"

    RSA_OAEP = (
        "cryptography.hazmat.primitives."
        "asymmetric.padding.OAEP"
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

    OPERATIONS = {
        "encrypt": CryptoOperation.ENCRYPT,
        "decrypt": CryptoOperation.DECRYPT,
    }

    def check(
        self,
        node: ast.AST,
        file_path: str,
        imports,
    ) -> list[Finding]:

        if not isinstance(node, ast.Call):
            return []

        if not isinstance(
            node.func,
            ast.Attribute,
        ):
            return []

        operation_name = node.func.attr

        operation = self.OPERATIONS.get(
            operation_name
        )

        if operation is None:
            return []

        padding_name = self._extract_padding(
            node,
            imports,
        )

        # Prevent unrelated .encrypt()/.decrypt()
        # methods from being classified as RSA.
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
                    "operation": operation.value,
                    "padding": padding_name,
                    "hash_algorithm": (
                        hash_algorithm
                    ),
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

            if resolved == self.RSA_OAEP:
                return "OAEP"

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

            resolved_padding = (
                self._resolve_function(
                    argument.func,
                    imports,
                    argument.lineno,
                )
            )

            if resolved_padding != self.RSA_OAEP:
                continue

            # OAEP normally stores its hash
            # configuration in keyword arguments.
            for keyword in argument.keywords:

                value = keyword.value

                if not isinstance(
                    value,
                    ast.Call,
                ):
                    continue

                resolved = self._resolve_function(
                    value.func,
                    imports,
                    value.lineno,
                )

                hash_name = (
                    self.HASH_ALGORITHMS.get(
                        resolved
                    )
                )

                if hash_name is not None:
                    return hash_name

        return None