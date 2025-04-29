import sys
import os
from configuration.config import Config
from git import Repo

from canvas_lms_api import CanvasClient, Course
    

def initialize_bin(config: Config):
    pass
    # os.makedirs(config.bin)



def initialize_course(config: Config):
    config.base.mkdir(parents=True, exist_ok=False)
    canvas_courses = list()
    for course_id in config.course_ids:
        canvas_courses.append(config.canvas_client._courses.get_course(course_id=course_id))
    for course in canvas_courses:
        print(course.id)
    

def main():
    if (config := Config.get_config()) is None:
        sys.exit("Missing configuration")
    initialize_course(config=config)
    initialize_bin(config=config)

if __name__ == "__main__":
    main()