from pathlib import Path


class FileDiscovery:
    """
    Responsible for discovering files inside a repository.
    """

    def discover_files(
        self,
        repository_path: Path,
    ) -> list[Path]:
        """
        Recursively discover all files.
        """

        files: list[Path] = []

        for path in repository_path.rglob("*"):

            if path.is_file():
                files.append(path)

        return files