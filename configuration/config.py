import os
import tomlkit
from pathlib import Path
from tomlkit import document, table, comment, dumps
from canvas_lms_api import CanvasClient
class Config:
    def __init__(self, class_code: str, bin: str, data: str, submissions: str, api_prefix: str, api_token: str, course_ids: list): 
        self.base = Path('/', 'cluster', 'pixstor', 'class', class_code)
        self.class_code = class_code
        self.bin = self.base / bin
        self.data = self.base / data
        self.submissions = self.base / submissions
        self.api_prefix = api_prefix
        self.api_token = api_token
        self.course_ids = course_ids
        self.canvas_client = CanvasClient(url_base=api_prefix, token=api_token)
    @staticmethod
    def prepare_toml_doc():
        doc = document()

        general = table()
        general.add(comment(" General MUCSv2 properties "))
        general.add(comment("   the class code you'll be backing up from."))
        general.add(comment(" valid options: cs1050, cs2050"))
        general.add("class_code", "")
    
        doc["general"] = general

        paths = table()
        paths.add(comment(" MUCSv2 is dependent on a set of directories. You can optionally configure the name of these directories."))
        paths.add(comment("    This directory stores the necessary (and optional) scripts needed for MUCSv2."))
        paths.add("bin", "bin")
        paths.add(comment("    This directory stores look-up tables related to Canvas data and other configuration properties."))
        paths.add("data", "data")
        paths.add(comment("    This directory stores student submissions related to the assignments you configured."))
        paths.add("submissions", "submissions")
        
        doc["paths"] = paths

        canvas = table()

        canvas.add(comment(" MUCSv2 uses Canvas as a remote ''database''. Your assignments, groups, and other data will be retrieved from there."))
        canvas.add(comment(" You can associate more than one Canvas course with your MUCSv2 course."))
        canvas.add(comment("    API Prefix for connecting to Canvas"))
        canvas.add(comment("    This shouldn't need to change for MUCS purposes"))
        canvas.add("api_prefix", "https://umsystem.instructure.com/api/v1/")
        canvas.add(comment(" API Token associated with your Canvas user"))
        canvas.add(comment(
            " https://community.canvaslms.com/t5/Canvas-Basics-Guide/How-do-I-manage-API-access-tokens-in-my-user-account/ta-p/615312"))
        canvas.add(comment(" You should keep this secret."))
        canvas.add("api_token", "")
        canvas.add(comment(" The Canvas course IDs associated with your course."))
        canvas.add("course_ids", [-1, -2])
        doc["canvas"] = canvas

        github_repos = table()
        github_repos.add(comment(" MUCSv2 pulls several modules from GitHub. You shouldn't need to change these, but you may use forks/different versions. "))
        github_repos.add(comment( "GenGraderTable"))
        github_repos.add("gen_grader_table", "https://github.com/Mizzou-CS-Core/GenGraderTable.git")
        github_repos.add("mucsmake", "https://github.com/Mizzou-CS-Core/MUCSMake.git")
        github_repos.add("gen_assignment_table", "https://github.com/Mizzou-CS-Core/LabWindowGen.git")




        with open("config.toml", 'w') as f:
            f.write(dumps(doc))
    @classmethod
    def get_config(cls):
        if not os.path.exists("config.toml"):
            cls.prepare_toml_doc()
            return None
        with open("config.toml", 'r') as f:
            content = f.read()
        doc = tomlkit.parse(content)

        # Extract values from the TOML document
        general = doc.get('general', {})
        paths = doc.get('paths', {})
        canvas = doc.get('canvas', {})

        return Config(
            class_code=general.get('class_code', ''),
            bin=paths.get('bin', 'bin'),
            data=paths.get('data', 'data'),
            submissions=paths.get('submissions', ''),
            api_prefix=canvas.get('api_prefix', ''),
            api_token=canvas.get('api_token', ''),
            course_ids=canvas.get('course_ids', [])
        )


    
