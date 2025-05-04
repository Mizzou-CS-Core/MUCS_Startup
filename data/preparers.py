import logging
from gen_assignment_window.gen_assignment_window import prepare_toml as prepare_assignment_toml, \
    prepare_assignment_window
from gen_grader_table.grader_table import generate_all_rosters, prepare_toml as prepare_roster_toml
from configuration.config import get_config
from canvas_lms_api import get_client
import mucs_database.store_objects as dao

from data.download import download_script

logger = logging.getLogger(__name__)


def prepare_assignment_table():
    config = get_config()
    canvas_assignment_name_predicate = input("Enter a canvas_assignment_name_predicate: ")
    blacklist = list(iter(lambda: input("Enter blacklist phrases (empty to stop): "), ""))
    gen_table = config.bin / "gen_assignment_table"
    logger.info(f"Config path is {gen_table}")
    prepare_assignment_toml(config_path=gen_table, canvas_token=config.api_token, canvas_course_id=config.course_ids[0],
                            canvas_assignment_name_predicate=canvas_assignment_name_predicate,
                            canvas_assignment_phrase_blacklist=blacklist, mucs_instance_code=config.class_code,
                            sqlite3_path=config.sqlite_db_path)
    for course_id in config.course_ids:
        prepare_assignment_window(canvas_course_id=course_id,
                                  canvas_assignment_name_predicate=canvas_assignment_name_predicate,
                                  canvas_assignment_phrase_blacklist=blacklist)


def prepare_grading_table():
    config = get_config()
    logger.info("Preparing grading tables")
    gen_table = config.bin / "gen_grader_table"
    logger.info(f"Config path is {gen_table}")
    prepare_roster_toml(mucsv2_instance_code=config.class_code, db_path=config.sqlite_db_path,
                        canvas_token=config.api_token, canvas_course_id=config.course_ids[0],
                        canvas_url_base=config.api_prefix, roster_invalidation_days=3, config_base=gen_table, )
    for course_id in config.course_ids:
        generate_all_rosters(course_id)


def prepare_course_data():
    config = get_config()
    dao.store_mucs_course()
    for course_id in config.course_ids:
        dao.store_canvas_course(course=get_client().courses.get_course(course_id=course_id))


def prepare_scripts():
    config = get_config()
    download_script(config.githubpaths.gen_assignment_table, "gen_assignment_table")
    download_script(config.githubpaths.gen_grader_table, "gen_grader_table")
