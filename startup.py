import sys
import os

from configuration.config import Config
from git import Repo
from database.init import init_database
from utilities.logger import info, warning, error


from canvas_lms_api import CanvasClient, Course
    

def initialize_bin(config: Config):
    pass
    # os.makedirs(config.bin)
def initialize_data(config: Config):
    info(f"Creating {config.data}")
    config.data.mkdir(parents=True, exist_ok=True)
    init_database(config=config)


def initialize_course(config: Config):
    info(f"Creating {config.base}")
    config.base.mkdir(parents=True, exist_ok=False)
    canvas_courses = list()
    for course_id in config.course_ids:
        info(f"Retrieving course data of {course_id} from Canvas")
        canvas_courses.append(config.canvas_client._courses.get_course(course_id=course_id))
    return canvas_courses
    

def main():
    if (config := Config.get_config()) is None:
        sys.exit("Missing configuration")
    canvas_courses = initialize_course(config=config)
    initialize_data(config=config)
    initialize_bin(config=config)

if __name__ == "__main__":
    main()