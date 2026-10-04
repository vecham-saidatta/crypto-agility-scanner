from app.services.repository_service import (
    prepare_repository_with_workspace,
)
from app.services.scanner_service import ScannerService
from app.services.workspace_service import WorkspaceService


class ScanService:
    """
    Coordinates repository preparation,
    scanning, and workspace cleanup.
    """

    def scan(
        self,
        repository_url: str,
    ) -> dict:

        prepared = prepare_repository_with_workspace(
            repository_url
        )

        workspace_service = WorkspaceService()

        try:
            scanner_service = ScannerService()

            return scanner_service.scan(
                prepared.repository_path
            )

        finally:
            workspace_service.cleanup_scan_workspace(
                prepared.workspace_path
            )
            