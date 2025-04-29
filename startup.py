import sys
import os
from configuration.config import Config
from git import Repo
    

def initialize_bin(config: Config):
    pass
    # os.makedirs(config.bin)



def initialize_course(config: Config):
    config.base.mkdir(parents=True, exist_ok=False)
    

def main():
    if (config := Config.get_config()) is None:
        sys.exit("Missing configuration")
    initialize_course(config=config)
    initialize_bin(config=config)

if __name__ == "__main__":
    main()