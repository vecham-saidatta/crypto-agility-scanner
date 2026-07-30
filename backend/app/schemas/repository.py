from pydantic import BaseModel, HttpUrl
from datetime import datetime
from pydantic import ConfigDict


class RepositoryCreate(BaseModel):
    name: str
    url: HttpUrl
    default_branch: str = "main"

class RepositoryUpdate(BaseModel):
    name: str
    url: HttpUrl
    default_branch: str

class RepositoryResponse(BaseModel):
    id: int
    name: str
    url: HttpUrl
    default_branch: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)