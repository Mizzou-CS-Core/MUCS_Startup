import logging
from colorama import Fore, Style
from gen_assignment_window.gen_assignment_window import prepare_toml as prepare_assignment_toml, \
    prepare_assignment_window
from gen_grader_table.grader_table import generate_all_rosters, prepare_toml as prepare_roster_toml
from mucsmake.configuration.config import prepare_toml_doc as prepare_mucsmake_toml
from configuration.config import get_config
from canvas_lms_api import get_client

import mucs_database.mucsv2_course.accessors as dao_mucsv2_course
import mucs_database.canvas_course.accessors as dao_canvas_course
import mucs_database.grading_group.accessors as dao_grading_group
import mucs_database.assignment.accessors as dao_assignment

from data.download import download_script

logger = logging.getLogger(__name__)


def prepare_submissions():
    logger.info("Preparing submissions directory")
    assignment_dict = dao_assignment.get_assignments()
    logger.debug(f"Assignment dict count: {len(assignment_dict)}")
    grading_group_dict = dao_grading_group.get_grading_groups()
    logger.debug(f"Grading group count: {len(grading_group_dict)}")
    for assignment in assignment_dict:
        assignment_dir = get_config().submissions / assignment['mucsv2_name']
        logger.debug(f"Creating {assignment_dir}")
        assignment_dir.mkdir(exist_ok=True, parents=True)
        for grading_group in grading_group_dict:
            group_dir = assignment_dir / grading_group['name']
            logger.debug(f"Creating {group_dir}")
            group_dir.mkdir(exist_ok=True, parents=True)


def prepare_test_files():
    logger.info("Preparing test files directory")
    assignment_dict = dao_assignment.get_assignments()
    logger.debug(f"Assignment dict count: {len(assignment_dict)}")
    test_files_dir = get_config().data / "test_files"
    logger.debug(f"Creating {test_files_dir}")
    test_files_dir.mkdir(exist_ok=True, parents=True)
    for assignment in assignment_dict:
        file_dir = test_files_dir / assignment['mucsv2_name']
        logger.debug(f"Creating {file_dir}")
        file_dir.mkdir(exist_ok=True, parents=True)


def prepare_assignment_table():
    config = get_config()
    name = "gen_assignment_table"
    logger.info(f"Preparing a standalone copy of {name}. This may take a while!")
    download_script(config.githubpaths.gen_assignment_table, directory_name=name)
    canvas_assignment_name_predicate = input(f"{Fore.BLUE}Enter a canvas_assignment_name_predicate: {Style.RESET_ALL}")
    blacklist = list(iter(lambda: input(f"{Fore.BLUE}Enter blacklist phrases (empty to stop): {Style.RESET_ALL}"), ""))
    gen_table = config.bin / name
    logger.debug(f"Config path is {gen_table}")
    prepare_assignment_toml(config_path=gen_table, canvas_token=config.api_token, canvas_course_id=config.course_ids[0],
                            canvas_assignment_name_predicate=canvas_assignment_name_predicate,
                            canvas_assignment_phrase_blacklist=blacklist, mucs_instance_code=config.class_code,
                            sqlite3_path=config.sqlite_db_path)
    for course_id in config.course_ids:
        prepare_assignment_window(canvas_course_id=course_id,
                                  canvas_assignment_name_predicate=canvas_assignment_name_predicate,
                                  canvas_assignment_phrase_blacklist=blacklist)


def prepare_mucsmake():
    config = get_config()
    name = "mucsmake"
    logger.info(f"Preparing a standalone copy of {name}. This may take a while!")
    download_script(config.githubpaths.mucsmake, directory_name=name)
    mucsmake = config.bin / name
    logger.debug(f"Config path is {mucsmake}")
    prepare_mucsmake_toml(mucsv2_instance_code=config.class_code, check_lab_header=True,
                          run_valgrind=True, base_path=config.base,
                          db_path=config.sqlite_db_path, lab_submission_directory=config.submissions,
                          test_files_directory=config.test_files)


def prepare_grading_table():
    config = get_config()
    name = "gen_grader_table"
    logger.info(f"Preparing a standalone copy of {name}. This may take a while!")
    download_script(config.githubpaths.gen_grader_table, directory_name=name)
    gen_table = config.bin / name
    logger.debug(f"Config path is {gen_table}")
    prepare_roster_toml(mucsv2_instance_code=config.class_code, db_path=config.sqlite_db_path,
                        canvas_token=config.api_token, canvas_course_id=config.course_ids[0],
                        canvas_url_base=config.api_prefix, roster_invalidation_days=3, config_base=gen_table, )
    for course_id in config.course_ids:
        generate_all_rosters(course_id)


def prepare_course_data():
    config = get_config()
    dao_mucsv2_course.store_mucs_course()
    for course_id in config.course_ids:
        course = get_client().courses.get_course(course_id=course_id)
        dao_canvas_course.store_canvas_course(canvas_id=course.id, name=course.course_code)
