import asyncio
import json
from pathlib import Path
import discord
from SplitFile import SplitFile


async def uploader(filePath):
    homeDir = str(Path.home())
    with open(f'{homeDir}/Library/Application Support/FileBreakerApp/userInfo.json', 'r') as json_file:
        userInfo = json.load(json_file)
    bot = discord.Client()
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
        # TODO: Include the message IDs with each piece so that the masterbot can more easily access stuff and speed up downloads soooo much
        await bot.close()
    await bot.start('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
