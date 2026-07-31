from abc import ABC, abstractmethod
from pathlib import Path

from app.scanners.findings import Finding


class BaseScanner(ABC):
    """
    Base class for all language scanners.
    """

    @abstractmethod
    def scan(
        self,
        files: list[Path],
    ) -> list[Finding]:
        """
        Scan a collection of files.
        """
        pass