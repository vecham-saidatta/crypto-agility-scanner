from abc import ABC, abstractmethod
from pathlib import Path


class BaseProvider(ABC):
    """
    Abstract base class for repository providers.
    """

    @abstractmethod
    def validate_repository_url(self, repository_url: str) -> bool:
        pass

    @abstractmethod
    def normalize_repository_url(self, repository_url: str) -> str:
        pass

    @abstractmethod
    def clone_repository(
        self,
        repository_url: str,
        workspace_path: Path,
    ) -> Path:
        pass

    @abstractmethod
    def delete_local_repository(
        self,
        repository_path: Path,
    ) -> None:
        pass