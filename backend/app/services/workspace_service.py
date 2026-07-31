from pathlib import Path
import uuid


class WorkspaceService:
    """
    Responsible for creating and managing scan workspaces.
    """

    def __init__(self):
        # backend/app/services -> backend -> project root
        self.project_root = Path(__file__).resolve().parents[3]
        self.workspace_root = self.project_root / "workspace"

        # Create workspace folder if it doesn't exist
        self.workspace_root.mkdir(exist_ok=True)

    def create_scan_workspace(self) -> Path:
        """
        Creates a unique workspace for a scan.
        """

        scan_id = uuid.uuid4().hex

        scan_path = self.workspace_root / scan_id

        scan_path.mkdir(parents=True, exist_ok=False)

        return scan_path