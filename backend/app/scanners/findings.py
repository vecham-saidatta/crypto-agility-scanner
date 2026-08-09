from dataclasses import dataclass, field
from typing import Any
from app.taxonomy.crypto_taxonomy import (
    normalize_algorithm,
    normalize_severity,
    normalize_status,
)

@dataclass
class Finding:

    algorithm: str
    file_path: str
    line_number: int
    severity: str
    status: str
    message: str
    recommendation: str
    reference: str

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    def __post_init__(self) -> None:

        self.algorithm = normalize_algorithm(
            self.algorithm
        )

        self.severity = normalize_severity(
            self.severity
        )

        self.status = normalize_status(
            self.status
        )