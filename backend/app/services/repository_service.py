from sqlalchemy.orm import Session
from typing import List
from app.models.repository import Repository
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryUpdate,
)


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