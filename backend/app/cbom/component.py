from dataclasses import dataclass, field
from typing import Any


@dataclass
class CBOMComponent:
    """
    Represents one cryptographic component
    discovered during repository scanning.
    """

    algorithm: str
    file: str
    line: int
    properties: dict[str, Any] = field(
        default_factory=dict
    )