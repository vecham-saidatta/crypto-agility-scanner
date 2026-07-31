'''from app.providers.azure_provider import AzureProvider
from app.providers.bitbucket_provider import BitbucketProvider
from app.providers.gitlab_provider import GitLabProvider'''  #temp


from app.providers.github_provider import GitHubProvider

class ProviderFactory:
    """
    Factory responsible for returning the correct repository provider.
    """

    @staticmethod
    def get_provider(repository_url: str):

        repository_url = repository_url.lower()

        if "github.com" in repository_url:
            return GitHubProvider()

        '''if "gitlab.com" in repository_url:
            return GitLabProvider()

        if "bitbucket.org" in repository_url:
            return BitbucketProvider()

        if "dev.azure.com" in repository_url:
            return AzureProvider()''' #temp

        raise ValueError(
            f"Unsupported repository provider: {repository_url}"
        )