from sqlalchemy.orm import Session
from typing import List
from app.models.repository import Repository
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryUpdate,
)
from pathlib import Path
from app.providers.provider_factory import ProviderFactory
from app.services.workspace_service import WorkspaceService


def create_repository(
    db: Session,
    repository: RepositoryCreate,
) -> Repository:
    new_repository = Repository(
        name=repository.name,
        url=str(repository.url),
        default_branch=repository.default_branch,
    )

    db.add(new_repository)
    db.commit()
    db.refresh(new_repository)

    return new_repository

def get_repositories(db: Session) -> List[Repository]:
    return db.query(Repository).all()

def get_repository_by_id(
    db: Session,
    repository_id: int,
):
    return (
        db.query(Repository)
        .filter(Repository.id == repository_id)
        .first()
    )

def update_repository(
    db: Session,
    repository: Repository,
    repository_data: RepositoryUpdate,
):
    repository.name = repository_data.name
    repository.url = str(repository_data.url)
    repository.default_branch = repository_data.default_branch

    db.commit()
    db.refresh(repository)

    return repository

def delete_repository(
    db: Session,
    repository: Repository,
):
    db.delete(repository)
    db.commit()

def prepare_repository_for_scan(
    repository_url: str,
) -> Path:
    """
    Prepare a repository for scanning.

    Steps:
    1. Create workspace.
    2. Select provider.
    3. Normalize URL.
    4. Validate URL.
    5. Clone repository.
    6. Return local repository path.
    """

    provider = ProviderFactory.get_provider(repository_url)

    repository_url = provider.normalize_repository_url(repository_url)

    if not provider.validate_repository_url(repository_url):
        raise ValueError("Invalid repository URL.")

    workspace_service = WorkspaceService()

    workspace_path = workspace_service.create_scan_workspace()

    repository_url = provider.normalize_repository_url(
        repository_url
    )

    if not provider.validate_repository_url(
        repository_url
    ):
        raise ValueError(
            "Invalid repository URL."
        )

    repository_path = provider.clone_repository(
        repository_url,
        workspace_path,
    )

    return repository_path