from pathlib import Path
from unittest.mock import patch

import pytest

from app.services.repository_resolver import (
    RepositoryResolver,
)


def test_resolves_existing_local_repository(
    tmp_path,
):
    repository = tmp_path / "repository"

    repository.mkdir()

    result = RepositoryResolver.resolve(
        str(repository)
    )

    assert result == repository


def test_rejects_existing_file(
    tmp_path,
):
    repository_file = (
        tmp_path / "repository.txt"
    )

    repository_file.write_text(
        "test",
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="must be a directory",
    ):
        RepositoryResolver.resolve(
            str(repository_file)
        )


def test_resolves_remote_repository():

    expected_path = (
        Path("workspace")
        / "cloned-repository"
    )

    with patch(
        "app.services.repository_resolver."
        "prepare_repository_for_scan"
    ) as prepare:

        prepare.return_value = (
            expected_path
        )

        result = (
            RepositoryResolver.resolve(
                "https://github.com/example/repository"
            )
        )

    assert result == expected_path

    prepare.assert_called_once_with(
        "https://github.com/example/repository"
    )


def test_rejects_missing_repository():

    with pytest.raises(
        ValueError,
        match="Repository path does not exist",
    ):
        RepositoryResolver.resolve(
            "does_not_exist"
        )