import json
import os
import sys
from pathlib import Path
import discord
from SplitFile import SplitFile


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    return os.path.join(os.path.dirname(sys.argv[0]), relative_path)


homeDir = str(Path.home())
with open(f'{homeDir}/Library/Application Support/FileBreakerApp/userInfo.json', 'r') as json_file:
    userInfo = json.load(json_file)
bot = discord.Client()
filePath = sys.argv[1]


@bot.event
async def on_ready():
    botChannel = await bot.fetch_channel(userInfo["botChannel"])
    await botChannel.send("This confirms that uploader is running")
    file = SplitFile(filePath)
    for name in file.chunkNames:
        fileObj = discord.File(
            open(f'{homeDir}/Library/Application Support/FileBreakerApp/filePieces/{name}', 'rb'),
            filename=name)
        await botChannel.send(file=fileObj)
    print("sent file")
    await botChannel.send(f'successfully uploaded:{file.fullName}')
    sys.exit()


bot.run('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
