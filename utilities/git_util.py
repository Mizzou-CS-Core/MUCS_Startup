from configuration.config import Config
def download_git_repo(config: Config, path):
    url, branch = str(path).split('@')
    logger.info(f"$download_git_repo: Cloning {url}@{branch} into {config.bin!r}")

    repo = Repo.clone_from(
        url         = url,
        to_path     = config.bin,
        branch      = branch,         # <-- check out this branch
        single_branch = True          # <-- only fetch that branch
    )
    return repo