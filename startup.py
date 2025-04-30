import sys
import os
import logging


from configuration.config import Config
from git import Repo
from database.init import init_database
from data.assignment_table import initialize_assignment_table, download_table_git_repo

from colorlog import ColoredFormatter

from canvas_lms_api import CanvasClient, Course
    
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



def initialize_bin(config: Config):
    logger.info(f"$initialize_bin: Creating {config.bin}")
    config.bin.mkdir(parents=True, exist_ok=True)
    download_table_git_repo(config=config)
    pass
    # os.makedirs(config.bin)
def initialize_data(config: Config):
    logger.info(f"$initialize_data: Creating {config.data}")
    config.data.mkdir(parents=True, exist_ok=True)
    init_database(config=config)
    initialize_assignment_table(config=config)



def initialize_course(config: Config):
    logger.info(f"Creating {config.base}")
    config.base.mkdir(parents=True, exist_ok=False)
    canvas_courses = list()
    for course_id in config.course_ids:
        logger.info(f"Retrieving course data of {course_id} from Canvas")
        canvas_courses.append(config.canvas_client._courses.get_course(course_id=course_id))
    return canvas_courses
    

def main():
    if (config := Config.get_config()) is None:
        sys.exit("Missing configuration")
    canvas_courses = initialize_course(config=config)
    initialize_data(config=config)
    initialize_bin(config=config)

if __name__ == "__main__":
    setup_logging()
    main()