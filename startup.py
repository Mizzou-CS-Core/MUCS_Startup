
from configuration.config import Config
    

  

def main():
    config = Config.get_config()
    if config is None:
        print("Missing configuration")

if __name__ == "__main__":
    main()