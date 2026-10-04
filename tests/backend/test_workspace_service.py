from pathlib import Path

import pytest

from app.services.workspace_service import (
    WorkspaceService,
)


def test_create_scan_workspace_creates_unique_directory(
    tmp_path,
):
    service = WorkspaceService()

    service.workspace_root = (
        tmp_path / "workspace"
    )
    service.workspace_root.mkdir()

    first = (
        service.create_scan_workspace()
    )

    second = (
        service.create_scan_workspace()
    )

    assert first.exists()
    assert first.is_dir()

    assert second.exists()
    assert second.is_dir()

    assert first != second


def test_cleanup_scan_workspace_removes_directory(
    tmp_path,
):
    service = WorkspaceService()

    service.workspace_root = (
        tmp_path / "workspace"
    )
    service.workspace_root.mkdir()

    scan_workspace = (
        service.create_scan_workspace()
    )

    repository = (
        scan_workspace / "repository"
    )
    repository.mkdir()

    (
        repository / "test.txt"
    ).write_text(
        "test",
        encoding="utf-8",
    )

    service.cleanup_scan_workspace(
        scan_workspace
    )

    assert not scan_workspace.exists()


def test_cleanup_missing_workspace_does_not_fail(
    tmp_path,
):
    service = WorkspaceService()

    service.workspace_root = (
        tmp_path / "workspace"
    )
    service.workspace_root.mkdir()

    missing_workspace = (
        service.workspace_root / "missing"
    )

    service.cleanup_scan_workspace(
        missing_workspace
    )


def test_cleanup_rejects_path_outside_workspace(
    tmp_path,
):
    service = WorkspaceService()

    service.workspace_root = (
        tmp_path / "workspace"
    )
    service.workspace_root.mkdir()

    outside_path = (
        tmp_path / "outside"
    )
    outside_path.mkdir()

    with pytest.raises(
        ValueError,
        match="outside workspace",
    ):
        service.cleanup_scan_workspace(
            outside_path
        )
def test_cleanup_scan_workspace_removes_read_only_file(
    tmp_path,
):
    service = WorkspaceService()

    service.workspace_root = (
        tmp_path / "workspace"
    )
    service.workspace_root.mkdir()

    scan_workspace = (
        service.create_scan_workspace()
    )

    read_only_file = (
        scan_workspace / "read_only.idx"
    )

    read_only_file.write_text(
        "git index data",
        encoding="utf-8",
    )

    read_only_file.chmod(0o444)

    service.cleanup_scan_workspace(
        scan_workspace
    )

    assert not scan_workspace.exists()
