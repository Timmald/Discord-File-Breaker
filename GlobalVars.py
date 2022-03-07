import json
from pathlib import Path
import os

homeDir = str(Path.home())  # homeDir, for example, is /Users/nathanwolf
appSupportFolder = f'/Library/Application Support/FileBreakerApp'
#TODO: This is the only apps upport folder everyone has, yet I don't have perms to write there I don't think?
currentChoicesPath = f'{appSupportFolder}/currentChoices.json'
userInfoPath = f'{appSupportFolder}/userInfo.json'
botChannelID = 939234547906777139
try:
    with open(currentChoicesPath, 'r') as json_file:
        fileList = json.load(json_file)
except FileNotFoundError:
    pass
downloadsFolder = f'{homeDir}/Downloads'