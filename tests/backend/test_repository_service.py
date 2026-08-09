from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from app.services.repository_service import (
    prepare_repository_for_scan,
)


def test_failed_clone_cleans_up_workspace(
    tmp_path,
):
    workspace_root = (
        tmp_path / "workspace"
    )

    workspace_root.mkdir()

    provider = Mock()

    provider.normalize_repository_url.return_value = (
        "https://github.com/example/repository.git"
    )

    provider.validate_repository_url.return_value = (
        True
    )

    provider.clone_repository.side_effect = (
        RuntimeError("clone failed")
    )

    with patch(
        "app.services.repository_service.ProviderFactory.get_provider",
        return_value=provider,
    ), patch(
        "app.services.repository_service.WorkspaceService"
    ) as workspace_class:

        workspace_service = (
            workspace_class.return_value
        )

        scan_workspace = (
            workspace_root / "scan"
        )

        scan_workspace.mkdir()

        workspace_service.create_scan_workspace.return_value = (
            scan_workspace
        )

        with pytest.raises(
            RuntimeError,
            match="clone failed",
        ):
            prepare_repository_for_scan(
                "https://github.com/example/repository"
            )

        workspace_service.cleanup_scan_workspace.assert_called_once_with(
            scan_workspace
        )