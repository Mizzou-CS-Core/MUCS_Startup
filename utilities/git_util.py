import logging

from git import Repo

from configuration.config import get_config

logger = logging.getLogger(__name__)


def download_git_repo(github_path, directory_name):
    config = get_config()
    url, branch = str(github_path).split('@')
    location = config.bin / directory_name
    logger.info(f"${download_git_repo.__name__}: Cloning {url}@{branch} into {location!r}")

    repo = Repo.clone_from(
        url=url,
        to_path=location,
        branch=branch,  # <-- check out this branch
        single_branch=True  # <-- only fetch that branch
    )
    return repo
