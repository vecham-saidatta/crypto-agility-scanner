from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import SessionLocal
from app.schemas.repository import (
    RepositoryCreate,
    RepositoryUpdate,
    RepositoryResponse,
)
from app.services.repository_service import (
    create_repository,
    get_repositories,
    get_repository_by_id,
    update_repository,
    delete_repository,
)


router = APIRouter(
    prefix="/repositories",
    tags=["Repositories"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post(
    "/",
    response_model=RepositoryResponse,
)
def create_repository_endpoint(
    repository: RepositoryCreate,
    db: Session = Depends(get_db),
):
    return create_repository(
        db=db,
        repository=repository,
    )

@router.get(
    "/",
    response_model=List[RepositoryResponse],
)
def get_repositories_endpoint(
    db: Session = Depends(get_db),
):
    return get_repositories(db=db)

@router.get(
    "/{repository_id}",
    response_model=RepositoryResponse,
)
def get_repository_by_id_endpoint(
    repository_id: int,
    db: Session = Depends(get_db),
):
    repository = get_repository_by_id(
        db=db,
        repository_id=repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    return repository

@router.put(
    "/{repository_id}",
    response_model=RepositoryResponse,
)
def update_repository_endpoint(
    repository_id: int,
    repository_data: RepositoryUpdate,
    db: Session = Depends(get_db),
):
    repository = get_repository_by_id(
        db=db,
        repository_id=repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    return update_repository(
        db=db,
        repository=repository,
        repository_data=repository_data,
    )

@router.delete(
    "/{repository_id}",
    status_code=204,
)
def delete_repository_endpoint(
    repository_id: int,
    db: Session = Depends(get_db),
):
    repository = get_repository_by_id(
        db=db,
        repository_id=repository_id,
    )

    if repository is None:
        raise HTTPException(
            status_code=404,
            detail="Repository not found",
        )

    delete_repository(
        db=db,
        repository=repository,
    )

    return
 