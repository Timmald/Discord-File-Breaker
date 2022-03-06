import json
from pathlib import Path

homeDir = str(Path.home())  # homeDir, for example, is /Users/nathanwolf
appSupportFolder = f'{homeDir}/Library/Application Support/FileBreakerApp'
currentChoicesPath = f'{appSupportFolder}/currentChoices.json'
userInfoPath = f'{appSupportFolder}/userInfo.json'
botChannelID = 939234547906777139
try:
    with open(currentChoicesPath, 'r') as json_file:
        fileList = json.load(json_file)
except FileNotFoundError:
    pass
downloadsFolder = f'{homeDir}/Downloads'