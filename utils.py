import json
import sys
from colorama import Fore

class Utils:
    def log(self, message: str):
       return sys.stdout.write(f'{Fore.CYAN}[MemberBackup]{Fore.CYAN}{Fore.RESET} {Fore.RED}» {message}\n')

    def LoadJson(self):
        with open('config.json', 'r') as f:
            return json.loads(f.read())

UtilsObject = Utils()