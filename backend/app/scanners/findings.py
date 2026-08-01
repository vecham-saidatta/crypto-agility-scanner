from dataclasses import dataclass


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