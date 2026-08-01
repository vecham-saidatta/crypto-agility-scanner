import ast

from app.scanners.findings import Finding
from app.scanners.python.rules.base_crypto_rule import BaseCryptoRule


class RSARule(BaseCryptoRule):

    algorithm = "RSA"
    function_name = "generate_private_key"

    allowed_modules = (
        "cryptography.hazmat.primitives.asymmetric.rsa",
    )

    severity = "INFO"
    status = "QUANTUM_VULNERABLE"

    message = "RSA key generation detected."

    recommendation = (
        "Inventory this RSA usage for post-quantum "
        "cryptography migration planning."
    )

    reference = "NIST FIPS 186-5"

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

        if (
            resolved_function
            != "cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key"
        ):
            return []

        key_size = None
        public_exponent = None

        for keyword in node.keywords:

            if keyword.arg == "key_size":
                if isinstance(keyword.value, ast.Constant):
                    key_size = keyword.value.value

            if keyword.arg == "public_exponent":
                if isinstance(keyword.value, ast.Constant):
                    public_exponent = keyword.value.value

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
                    "key_size": key_size,
                    "public_exponent": public_exponent,
                },
            )
        ]