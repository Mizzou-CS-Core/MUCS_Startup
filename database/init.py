import sqlite3
from utilities.logger import info, warning, error

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



def init_database(config: Config):
    db_name = f"{config.data}{config.sqlite_db}.db"
    print(db_name)
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor
            for statement in sql_statements:
                cursor.execute(statement)
            conn.commit()

    except sqlite3.OperationalError as e:
        error(f"Failed to open database: {e}")

