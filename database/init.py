import sqlite3
import logging
from configuration.config import Config

logger = logging.getLogger(__name__)

sql_statements = [
    """CREATE TABLE IF NOT EXISTS mucsv2_course (
    course_code     TEXT    PRIMARY KEY
    );""",

    """CREATE TABLE IF NOT EXISTS canvas_course (
    canvas_id           INTEGER PRIMARY KEY,
    mucs_course_code    TEXT    NOT NULL,
    name                TEXT    NOT NULL,
    FOREIGN KEY (mucs_course_code)
        REFERENCES mucsv2_course(course_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );""",
    """CREATE TABLE IF NOT EXISTS graders (
    canvas_id           INTEGER PRIMARY KEY,
    canvas_course_id    INTEGER NOT NULL,
    name                TEXT    NOT NULL,
    FOREIGN KEY (canvas_course_id)
        REFERENCES canvas_course(canvas_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );""",
    """CREATE TABLE IF NOT EXISTS students (
    canvas_id   INTEGER PRIMARY KEY,
    grader_id   INTEGER NOT NULL,
    name        TEXT    NOT NULL,
    pawprint    TEXT,
    FOREIGN KEY (grader_id)
        REFERENCES graders(canvas_id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );""",
    """CREATE TABLE IF NOT EXISTS assignments (
    canvas_id        INTEGER PRIMARY KEY,
    mucs_course_code TEXT    NOT NULL,
    name             TEXT,
    open_at          DATE,
    due_at           DATE    NOT NULL,
    FOREIGN KEY (mucs_course_code)
        REFERENCES mucsv2_course(course_code)
        ON DELETE CASCADE
        ON UPDATE CASCADE
    );"""
]

def get_cursor(config: Config):
    try:
        with sqlite3.connect(config.sqlite_db_path) as conn:
            return conn.cursor()
    except sqlite3.OperationalError as e:
        logger.error(f"{e}")

def init_database(config: Config):
    logger.info(f"$init_database: Initializing {config.sqlite_db_path} as SQLite3 DB")
    try:
        with sqlite3.connect(config.sqlite_db_path) as conn:
            cursor = conn.cursor()
            for statement in sql_statements:
                cursor.execute(statement)
            conn.commit()

    except sqlite3.OperationalError as e:
        logger.error(f"{e}")
    

