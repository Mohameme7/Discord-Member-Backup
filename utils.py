import json
import sys
from colorama import Fore


def log(message: str):
   return sys.stdout.write(f'{Fore.CYAN}[MemberBackup]{Fore.CYAN}{Fore.RESET} {Fore.RED}» {message}\n')

def LoadJson():
    with open('config.json', 'r') as f:
        return json.load(f)

