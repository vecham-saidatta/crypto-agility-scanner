from fastapi import APIRouter

from app.schemas.scan import (
    ScanRequest,
    ScanResponse,
)

from app.services.repository_service import (
    prepare_repository_for_scan,
)

router = APIRouter(
    prefix="/scans",
    tags=["Scans"],
)


@router.post(
    "",
    response_model=ScanResponse,
)
def start_scan(
    request: ScanRequest,
):

    repository_path = prepare_repository_for_scan(
        str(request.repository_url)
    )

    return ScanResponse(
        status="Repository Ready for Scanning",
        repository_path=str(repository_path),
    )