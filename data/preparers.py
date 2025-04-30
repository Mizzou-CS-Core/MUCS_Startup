import logging
from gen_assignment_window.gen_lab_window import initialize_window
from configuration.config import Config
from git import Repo
from canvas_lms_api import get_client
import mucs_database.store_objects as dao
logger = logging.getLogger(__name__)


def prepare_assignment_table(config: Config):
    cursor = get_cursor(config=config)
    canvas_assignment_name_predicate = input("Enter a canvas_assignment_name_predicate: ")
    blacklist = list(iter(lambda: input("Enter (empty to stop): "), ""))
    gen_table = config.data / "gen_assignment_table"
    logger.info(f"Config path is {gen_table}")
    gen_table.mkdir()
    initialize_window(cursor=cursor, config_path=gen_table, canvas_token=config.api_token, canvas_course_id=config.course_ids[0], canvas_assignment_name_predicate=canvas_assignment_name_predicate, canvas_assignment_phrase_blacklist=blacklist, mucs_course_code=config.class_code)
def prepare_course_data(config: Config):
    dao.store_mucs_course()
    for course_id in config.course_ids:
        dao.store_canvas_course(course=get_client()._courses.get_course(course_id=course_id))