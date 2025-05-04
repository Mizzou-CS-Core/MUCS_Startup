import logging
import venv
from utilities.git_util import download_git_repo
from configuration.config import get_config

logger = logging.getLogger(__name__)


def download_virtual_env(directory):
    pass


def download_assignment_table_script():
    config = get_config()
    logger.info(f"Downloading {config.githubpaths.gen_assignment_table}")
    download_git_repo(config.githubpaths.gen_assignment_table, "gen_assignment_table}")


