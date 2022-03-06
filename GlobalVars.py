import json
from pathlib import Path

homeDir = str(Path.home())  # homeDir, for example, is /Users/nathanwolf
appSupportFolder = f'{homeDir}/Library/Application Support/FileBreakerApp'
currentChoicesPath = f'{appSupportFolder}/currentChoices.json'
userInfoPath = f'{appSupportFolder}/userInfo.json'
botChannelID = 939234547906777139
with open(currentChoicesPath, 'r') as json_file:
    fileList = json.load(json_file)
downloadsFolder = f'{homeDir}/Downloads'