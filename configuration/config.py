import os
import tomlkit
from tomlkit import document, table, comment, dumps
import logging

from configuration.models import GitHubPaths, Config

logger = logging.getLogger(__name__)

_config = None


def prepare_toml_doc():
    doc = document()

    general = table()
    general.add(comment(" General MUCSv2 properties "))
    general.add(comment("   the class code you'll be backing up from."))
    general.add(comment(" valid options: cs1050, cs2050"))
    general.add("class_code", "")
    general.add(comment(" The name of the SQLite database. "))
    general.add(comment("If left blank, it'll default to the class code you set."))
    general.add("sqlite_db", "")

    doc["general"] = general

    paths = table()
    paths.add(comment(
        " MUCSv2 is dependent on a set of directories. You can optionally configure the name of these directories."))
    paths.add(comment("    This directory stores the necessary (and optional) scripts needed for MUCSv2."))
    paths.add("bin", "bin")
    paths.add(
        comment("    This directory stores look-up tables related to Canvas data and other configuration properties."))
    paths.add("data", "data")
    paths.add(comment("    This directory stores student submissions related to the assignments you configured."))
    paths.add("submissions", "submissions")

    doc["paths"] = paths

    canvas = table()

    canvas.add(comment(
        "MUCSv2 uses Canvas as a remote ''database''. Your assignments, groups, and other data will be retrieved from "
        "there."))
    canvas.add(comment(" You can associate more than one Canvas course with your MUCSv2 course."))
    canvas.add(comment("    API Prefix for connecting to Canvas"))
    canvas.add(comment("    This shouldn't need to change for MUCS purposes"))
    canvas.add("api_prefix", "https://umsystem.instructure.com/api/v1/")
    canvas.add(comment(" API Token associated with your Canvas user"))
    canvas.add(comment(
        "https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account"
        "/ta-p/615312"))
    canvas.add(comment(" You should keep this secret."))
    canvas.add("api_token", "")
    canvas.add(comment(" The Canvas course IDs associated with your course."))
    canvas.add("course_ids", [-1, -2])
    doc["canvas"] = canvas

    github_repos = table()
    github_repos.add(comment(
        "MUCSv2 pulls several modules from GitHub. You shouldn't need to change these, but you may use "
        "forks/different versions. "))
    github_repos.add(comment("GenGraderTable"))
    github_repos.add("gen_grader_table", "https://github.com/Mizzou-CS-Core/GenGraderTable.git@sql_integration")
    github_repos.add("mucsmake", "https://github.com/Mizzou-CS-Core/MUCSMake.git@sql_integration")
    github_repos.add("gen_assignment_table", "https://github.com/Mizzou-CS-Core/LabWindowGen.git@sql-integration")
    doc['github_repos'] = github_repos

    with open("config.toml", 'w') as f:
        f.write(dumps(doc))


def get_config() -> Config:
    if _config is None:
        logger.error("The configuration file has not been loaded into memory!")
    return _config


def initialize_config():
    global _config
    if not os.path.exists("config.toml"):
        logger.warning("An existing configuration file did not exist.")
        prepare_toml_doc()
        return None
    with open("config.toml", 'r') as f:
        logger.info("Reading config.toml into memory")
        content = f.read()
    doc = tomlkit.parse(content)

    # Extract values from the TOML document
    general = doc.get('general', {})
    paths = doc.get('paths', {})
    canvas = doc.get('canvas', {})
    github_repos = doc.get('github_repos', {})
    github = GitHubPaths(gen_grader_table=github_repos.get('gen_grader_table'), mucsmake=github_repos.get('mucsmake'),
                         gen_assignment_table=github_repos.get('gen_assignment_table'))

    _config = Config(class_code=general.get('class_code', ''), bin=paths.get('bin', 'bin'),
                     data=paths.get('data', 'data'), submissions=paths.get('submissions', ''),
                     api_prefix=canvas.get('api_prefix', ''), api_token=canvas.get('api_token', ''),
                     course_ids=canvas.get('course_ids', []), sqlite_db=general.get('sqlite_db', ''),
                     githubpaths=github)
