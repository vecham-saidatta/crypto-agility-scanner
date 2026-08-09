from pathlib import Path

from app.services.repository_service import (
    prepare_repository_for_scan,
)


class RepositoryResolver:
    """
    Resolves local repository paths and
    supported remote repository URLs.
    """

    @staticmethod
    def resolve(
        repository: str,
    ) -> Path:

        repository_path = Path(
            repository
        )

        if repository_path.exists():

            if not repository_path.is_dir():
                raise ValueError(
                    "Repository path must be a directory."
                )

            return repository_path

        if (
            repository.startswith("http://")
            or repository.startswith("https://")
        ):
            return prepare_repository_for_scan(
                repository
            )

        raise ValueError(
            "Repository path does not exist: "
            f"{repository}"
        )