from pathlib import Path

import pytest

from app.providers.github_provider import (
    GitHubProvider,
)


@pytest.fixture
def provider():
    return GitHubProvider()


def test_valid_github_repository_url(provider):
    assert provider.validate_repository_url(
        "https://github.com/owner/repository"
    )


def test_valid_github_repository_url_with_git_suffix(
    provider,
):
    assert provider.validate_repository_url(
        "https://github.com/owner/repository.git"
    )


@pytest.mark.parametrize(
    "repository_url",
    [
        "https://github.com/",
        "https://github.com//",
        "https://github.com/owner",
        "http://github.com/owner/repository",
        "https://gitlab.com/owner/repository",
        "not-a-url",
    ],
)
def test_invalid_github_repository_urls(
    provider,
    repository_url,
):
    assert not provider.validate_repository_url(
        repository_url
    )


def test_normalize_github_repository_url(provider):
    assert (
        provider.normalize_repository_url(
            "https://github.com/owner/repository"
        )
        == "https://github.com/owner/repository.git"
    )


def test_normalize_github_repository_url_keeps_git_suffix(
    provider,
):
    assert (
        provider.normalize_repository_url(
            "https://github.com/owner/repository.git"
        )
        == "https://github.com/owner/repository.git"
    )