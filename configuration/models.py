from pathlib import Path


class GitHubPaths:
    def __init__(self, gen_grader_table, mucsmake, gen_assignment_table):
        self.gen_grader_table = gen_grader_table
        self.mucsmake = mucsmake
        self.gen_assignment_table = gen_assignment_table


class Config:
    def __init__(self, class_code: str, bin: str, data: str, submissions: str, api_prefix: str, api_token: str,
                 course_ids: list, sqlite_db: str, githubpaths: GitHubPaths, test_files=""):
        self.base = Path('/', 'cluster', 'pixstor', 'class', class_code)
        self.class_code = class_code
        self.bin = self.base / bin
        self.data = self.base / data
        self.submissions = self.base / submissions
        self.api_prefix = api_prefix
        self.api_token = api_token
        self.course_ids = course_ids
        self.sqlite_db = self.class_code if sqlite_db == "" else sqlite_db
        self.sqlite_db_path = f"{self.data}/{self.sqlite_db}.db"
        self.githubpaths = githubpaths
        self.test_files = test_files
