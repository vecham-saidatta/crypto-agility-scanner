from pydantic import BaseModel, HttpUrl


class ScanRequest(BaseModel):
    repository_url: HttpUrl


class ScanResponse(BaseModel):
    status: str
    repository_path: str