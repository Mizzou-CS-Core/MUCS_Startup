import logging
import subprocess
import sys
import venv
from pathlib import Path
from utilities.git_util import download_git_repo

logger = logging.getLogger(__name__)


class MUCSEnvBuilder(venv.EnvBuilder):
    def __init__(self, with_pip=True, requirements_in: str = "requirements.in",
                 name_repo: str = "", **envbuilder_kargs):
        super().__init__(with_pip=with_pip, **envbuilder_kargs)
        self.requirements_in = Path(requirements_in)
        self.name_repo = name_repo

    def post_setup(self, context):
        logger.debug(f"Attempting post-install setup for {self.name_repo}")
        if not self.requirements_in.exists():
            raise FileNotFoundError(f"${self.name_repo}: {self.requirements_in} not found")
        logger.debug(f"${self.name_repo}: Compiling {self.requirements_in}")
        result = subprocess.run([sys.executable, "-m", "piptools", "compile",
                                 str(self.requirements_in), "--output-file", "requirements.txt"], capture_output=True,
                                text=True)
        python_exe = context.env_exe
        logger.debug(f"${self.name_repo}: Installing requirements.txt into {python_exe}")
        result = subprocess.run([python_exe, "-m", "pip", "install", "-r", "requirements.txt"],
                                capture_output=True, text=True)


def download_virtual_env(directory: Path):
    logger.debug(f"Creating virtual environment in {directory}")
    builder = MUCSEnvBuilder(with_pip=True, name_repo=str(directory / ".venv"))
    builder.create(directory / ".venv")


def download_script(git_path: str, directory_name):
    logger.info(f"Downloading {git_path}")
    path = download_git_repo(github_path=git_path, directory_name=directory_name)
    logger.info(f"Creating virtual environment for {path}")
    download_virtual_env(directory=path)
