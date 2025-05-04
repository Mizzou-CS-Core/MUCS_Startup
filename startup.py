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
    prepare_grading_table,
)

config: Config


def setup_logging():
    # everything including debug goes to log file
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    fh = logging.FileHandler("mucs_startup.log", encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s"
    ))
    # log info and above to console
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # this format string lets colorlog insert color around the whole line
    fmt = "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    colors = {
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'bold_red',
    }
    ch.setFormatter(ColoredFormatter(fmt, log_colors=colors))
    root.addHandler(fh)
    root.addHandler(ch)


logger = logging.getLogger(__name__)


def initialize_bin_directory():
    logger.debug(f"${initialize_bin_directory.__name__}: Creating {config.bin}")
    config.bin.mkdir(parents=True, exist_ok=True)


def initialize_data_directory():
    logger.debug(f"${initialize_data_directory.__name__}: Creating {config.data}")
    config.data.mkdir(parents=True, exist_ok=True)


def initialize_course_directory():
    logger.debug(f"${initialize_course_directory.__name__}: Creating {config.base}")
    config.base.mkdir(parents=True, exist_ok=False)


def initalize_submissions_directory():
    logger.debug(f"${initalize_submissions_directory.__name__}: Creating {config.submissions}")
    config.submissions.mkdir(parents=True, exist_ok=True)


def initialize_directories():
    logger.info("Initializing required directories")
    initialize_course_directory()
    initialize_bin_directory()
    initialize_data_directory()
    initalize_submissions_directory()


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
