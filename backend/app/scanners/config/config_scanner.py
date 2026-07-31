from pathlib import Path

from app.scanners.base_scanner import BaseScanner
from app.scanners.findings import Finding


class ConfigScanner(BaseScanner):

    def scan(
        self,
        files: list[Path],
    ) -> list[Finding]:

        return []