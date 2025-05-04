import logging
import sys

from canvas_lms_api import init as initialize_canvas_client
from colorlog import ColoredFormatter
from mucs_database.init import initialize_database

from configuration.config import initialize_config, get_config
from configuration.models import Config
from data.preparers import (
    prepare_assignment_table,
    prepare_course_data,
    prepare_grading_table)

config: Config


def setup_logging():
    handler = logging.StreamHandler()
    # this format string lets colorlog insert color around the whole line
    fmt = "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    handler.setFormatter(ColoredFormatter(fmt, log_colors=colors))
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)


logger = logging.getLogger(__name__)


def initialize_bin_directory():
    logger.debug(f"$initialize_bin_directory: Creating {config.bin}")
    config.bin.mkdir(parents=True, exist_ok=True)
    # download_git_repo(config=config, path=config.githubpaths.gen_assignment_table)


def initialize_data_directory():
    logger.debug(f"$initialize_data_directory: Creating {config.data}")
    config.data.mkdir(parents=True, exist_ok=True)


def initialize_course_directory():
    logger.debug(f"$initialize_course_directory: Creating {config.base}")
    config.base.mkdir(parents=True, exist_ok=False)


def initialize_directories():
    logger.info("Initializing required directories")
    initialize_course_directory()
    initialize_bin_directory()
    initialize_data_directory()


def sign_as_mucsv2_course():
    logger.info("Signing course as MUCSv2 Enabled")
    filename = config.base / "mucsv2.info"
    logger.debug(f"{sign_as_mucsv2_course.__name__}: Creating file as {filename}")
    filename.touch()
    logger.debug(f"{sign_as_mucsv2_course.__name__}: Created file as {filename}")


def prepare_data():
    sign_as_mucsv2_course()

    prepare_course_data()
    prepare_assignment_table()
    prepare_grading_table()


def main():
    initialize_config()
    global config
    if (config := get_config()) is None:
        sys.exit("Missing configuration")
    initialize_directories()
    initialize_database(sqlite_db_path=config.sqlite_db_path, mucsv2_instance_code=config.class_code)
    initialize_canvas_client(url_base=config.api_prefix, token=config.api_token)

    prepare_data()


if __name__ == "__main__":
    setup_logging()
    main()
