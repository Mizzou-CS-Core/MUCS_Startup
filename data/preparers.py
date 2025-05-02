import logging
from gen_assignment_window.gen_lab_window import prepare_assignment_window_and_config
from gen_grader_table.grader_table import generate_all_rosters, prepare_toml
from configuration.config import Config
from canvas_lms_api import get_client
import mucs_database.store_objects as dao

logger = logging.getLogger(__name__)


def prepare_assignment_table(config: Config):
    canvas_assignment_name_predicate = input("Enter a canvas_assignment_name_predicate: ")
    blacklist = list(iter(lambda: input("Enter (empty to stop): "), ""))
    gen_table = config.data / "gen_assignment_table"
    logger.info(f"Config path is {gen_table}")
    gen_table.mkdir()
    prepare_assignment_window_and_config(config_path=gen_table, canvas_token=config.api_token,
                                         canvas_course_id=config.course_ids,
                                         canvas_assignment_name_predicate=canvas_assignment_name_predicate,
                                         canvas_assignment_phrase_blacklist=blacklist,
                                         mucs_instance_code=config.class_code, sqlite3_path=config.sqlite_db_path)


def prepare_grading_table(config: Config):
    logger.info("Preparing grading tables")
    gen_table = config.data / "gen_grading_table"
    logger.info(f"Config path is {gen_table}")
    gen_table.mkdir()
    prepare_toml(mucsv2_instance_code=config.class_code, db_path=config.sqlite_db_path,
                 canvas_token=config.api_token, canvas_course_id=config.course_ids[0],
                 canvas_url_base=config.api_prefix, roster_invalidation_days=3, config_base= gen_table, )
    for course_id in config.course_ids:
        generate_all_rosters(course_id)


def prepare_course_data(config: Config):
    dao.store_mucs_course()
    for course_id in config.course_ids:
        dao.store_canvas_course(course=get_client()._courses.get_course(course_id=course_id))
