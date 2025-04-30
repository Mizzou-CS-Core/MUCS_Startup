import sys
import os
import logging


from configuration.config import Config
from data.preparers import prepare_assignment_table, prepare_course_data
from utilities.git_util import download_git_repo
from colorlog import ColoredFormatter

from mucs_database.init import initialize_database
import mucs_database.store_objects as dao

from canvas_lms_api import init as initialize_canvas_client
    
def setup_logging():
    handler = logging.StreamHandler()
    # this format string lets colorlog insert color around the whole line
    fmt = "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    colors = {
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
    handler.setFormatter(ColoredFormatter(fmt, log_colors=colors))
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(handler)

logger = logging.getLogger(__name__) 



def initialize_bin_directory(config: Config):
    logger.debug(f"$initialize_bin_directory: Creating {config.bin}")
    config.bin.mkdir(parents=True, exist_ok=True)
    # download_git_repo(config=config, path=config.githubpaths.gen_assignment_table)
def initialize_data_directory(config: Config):
    logger.debug(f"$initialize_data_directory: Creating {config.data}")
    config.data.mkdir(parents=True, exist_ok=True)
def initialize_course_directory(config: Config):
    logger.debug(f"$initialize_course_directory: Creating {config.base}")
    config.base.mkdir(parents=True, exist_ok=False)
    

def initialize_directories(config: Config):
    logger.info("Initializing required directories")
    initialize_course_directory(config=config)
    initialize_bin_directory(config=config)
    initialize_data_directory(config=config)

def prepare_data(config: Config):
    prepare_course_data(config=config)
    prepare_assignment_table(config=config)


def main():
    if (config := Config.get_config()) is None:
        sys.exit("Missing configuration")
    initialize_directories(config=config)
    initialize_database(sqlite_db_path=config.sqlite_db_path, class_code=config.class_code)
    initialize_canvas_client(url_base=config.api_prefix, token=config.api_token)

    prepare_data(config=config)


if __name__ == "__main__":
    setup_logging()
    main()