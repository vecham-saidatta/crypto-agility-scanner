from pathlib import Path
import shutil

from git import Repo
from git.exc import GitCommandError

from app.providers.base_provider import BaseProvider


class GitHubProvider(BaseProvider):
    """
    GitHub repository provider.
    """

    def validate_repository_url(self, repository_url: str) -> bool:
        return repository_url.startswith("https://github.com/")

    def normalize_repository_url(self, repository_url: str) -> str:
        repository_url = repository_url.strip()

        if not repository_url.endswith(".git"):
            repository_url += ".git"

        return repository_url

    def clone_repository(
        self,
        repository_url: str,
        workspace_path: Path,
    ) -> Path:

        repository_path = workspace_path / "repository"

        try:
            Repo.clone_from(
                repository_url,
                repository_path,
            )

            return repository_path

        except GitCommandError as error:
            raise Exception(
                f"Failed to clone repository: {error}"
            )

    def delete_local_repository(
        self,
        repository_path: Path,
    ) -> None:

        if repository_path.exists():
            shutil.rmtree(repository_path)