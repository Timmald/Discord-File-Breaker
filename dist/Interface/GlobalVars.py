import json
from pathlib import Path
import os

homeDir = str(Path.home())  # homeDir, for example, is /Users/nathanwolf
appSupportFolder = f'{homeDir}/Library/Application Support/FileBreakerApp'
libraryPath = f'{homeDir}/Library'
if not os.path.exists(libraryPath):
    os.mkdir(libraryPath)
appSupport = os.path.dirname(appSupportFolder)
if not os.path.exists(appSupport):
    os.mkdir(appSupport)
currentChoicesPath = f'{appSupportFolder}/currentChoices.json'
userInfoPath = f'{appSupportFolder}/userInfo.json'
botChannelID = 939234547906777139
try:
    with open(currentChoicesPath, 'r') as json_file:
        fileList = json.load(json_file)
except FileNotFoundError:
    pass
downloadsFolder = f'{homeDir}/Downloads'