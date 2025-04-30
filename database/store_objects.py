from canvas_lms_api import Course
from configuration.config import Config
import logging
import sqlite3
logger = logging.getLogger(__name__)

def get_cursor(config: Config):
    logger.debug("Retrieving cursor")
    try:
        with sqlite3.connect(config.sqlite_db_path) as conn:
            return conn.cursor()
    except sqlite3.OperationalError as e:
        logger.error(f"{e}")

def store_canvas_course(config: Config, course: Course):
    sql = "INSERT INTO canvas_course(canvas_id, mucs_course_code, name) VALUES (?, ?, ?)"
    logger.debug(f"Storing a Course with Canvas ID: {course.id}")
    cursor = get_cursor(config=config)
    row = (course.id, config.class_code, course.name)
    try:
        cursor.execute(sql, row)
        cursor.connection.commit()
    except sqlite3.OperationalError as e:
        logger.error(f"Failed to insert row {row}: {e}")
def store_mucs_course(config: Config):
    sql = "INSERT INTO mucsv2_course(course_code) VALUES (?)"
    logger.debug(f"Storing a MUCSv2 Course with code: {config.class_code}")
    cursor = get_cursor(config=config)
    row = (config.class_code,)
    try:
        cursor.execute(sql, row)
        cursor.connection.commit()
    except sqlite3.OperationalError as e:
        logger.error(f"Failed to insert row {row}: {e}")


