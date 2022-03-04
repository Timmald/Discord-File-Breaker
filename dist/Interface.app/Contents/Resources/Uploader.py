import os
import sys
import time
import json
import datetime
from datetime import timezone
from zoneinfo import ZoneInfo

import discord

from SplitFile import SplitFile

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    return os.path.join(os.path.dirname(sys.argv[0]),relative_path)

userName=os.path.normpath(sys.argv[0]).split(os.path.sep)[2]
with open(f'/Users/{userName}/Library/Application Support/FileBreakerApp/userInfo.json', 'r') as json_file:
    userInfo = json.load(json_file)

#def uploadFile(filepath: os.PathLike):
bot = discord.Client()
filePath = sys.argv[1]
@bot.event
async def on_ready():
    global uploadedFiles
    botChannel = await bot.fetch_channel(userInfo["botChannel"])
    await botChannel.send("This confirms that uploader is running")
    file = SplitFile(filePath)
    for name in file.chunkNames:
        fileObj = discord.File(
            open(f'/Users/{userInfo["userName"]}/Library/Application Support/FileBreakerApp/filePieces/{name}', 'rb'),
            filename=name)
        await botChannel.send(file=fileObj)
    print("sent file")
    await botChannel.send(f'successfully uploaded:{file.fullName}')
    #uploadedFiles+=[[f'{file.name}; Uploaded at {datetime.datetime.now(tz=ZoneInfo("America/New_York")).strftime("%c")}',len(file.chunkNames)]]
    # with open('filePieces.json','w') as json_file:
    #     json.dump(uploadedFiles,json_file,indent=0)
    sys.exit()
bot.run('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
