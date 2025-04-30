from colorama import Fore
from colorama import Style

def info(message: str):
    print(f"{Fore.BLUE}INFO: {message}{Style.RESET_ALL}")
def warning(message: str):
    print(f"{Fore.YELLOW}WARNING: {message}{Style.RESET_ALL}")
def error(message: str):
    print(f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}")

    