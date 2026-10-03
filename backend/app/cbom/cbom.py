from dataclasses import dataclass, field

from app.cbom.component import CBOMComponent


@dataclass
class CBOM:
    """
    Represents the cryptographic inventory
    for a scan.
    """

    components: list[CBOMComponent] = field(
        default_factory=list
    )