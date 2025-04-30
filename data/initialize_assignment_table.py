import logging
from gen_assignment_window.gen_lab_window import initialize_window
from configuration.config import Config

from database.init import get_cursor
logger = logging.getLogger(__name__)


def initialize_assignment_table(config: Config):
    cursor = get_cursor(config=config)
    canvas_assignment_name_predicate = input("Enter a canvas_assignment_name_predicate: ")
    blacklist = list(iter(lambda: input("Enter (empty to stop): "), ""))
    gen_table = config.data / "gen_table"
    logger.info(f"Config path is {gen_table}")
    gen_table.mkdir()
    initialize_window(cursor=cursor, config_path=gen_table, canvas_token=config.api_token, canvas_course_id=config.course_ids[0], canvas_assignment_name_predicate=canvas_assignment_name_predicate, canvas_assignment_phrase_blacklist=blacklist, mucs_course_code=config.class_code)

