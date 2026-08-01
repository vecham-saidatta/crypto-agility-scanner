from dataclasses import dataclass, field
from typing import Any


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