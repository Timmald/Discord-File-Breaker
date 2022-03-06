import json
import os
from pathlib import Path
from ssl import SSLCertVerificationError
import discord
import sys
from datetime import datetime, timezone


async def query():
    client = discord.Client()
    homeDir = str(Path.home())
    appSupportFolder = f'{homeDir}/Library/Application Support/FileBreakerApp'
    with open(f'{appSupportFolder}/userInfo.json', 'r') as json_file:
        userInfo = json.load(json_file)

    @client.event
    async def on_ready():
        botChannel = await client.fetch_channel(userInfo["botChannel"])
        await botChannel.send('$downloadList')

    @client.event
    async def on_message(message):
        if message.author.id == 937444289208778782:
            downloadChoices = message.content
            currentChoicesPath = f'{appSupportFolder}/currentChoices.json'
            with open(currentChoicesPath, 'w') as json_file:
                json.dump(json.loads(downloadChoices), json_file, indent=0)
            await client.close()

    await client.start('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
    return


async def download(fileName, pieceNum):
    client = discord.Client()
    homeDir = str(Path.home())
    downloads = f'{homeDir}/Downloads'
    appSupportFolder = f'{homeDir}/Library/Application Support/FileBreakerApp'
    with open(f'{appSupportFolder}/userInfo.json', 'r') as json_file:
        userInfo = json.load(json_file)

    @client.event
    async def on_ready():
        print('yo')
        botChannel = await client.fetch_channel(userInfo["botChannel"])
        fileData = fileName.split(';_Uploaded_at_')
        fileData[1] = datetime.strptime(fileData[1].replace('_', ' '), '%c')
        pieceNames = [f'{fileData[0]} piece {i}.txt'.replace(' ', '_') for i in range(1, pieceNum + 1)]
        # oh how I wish we could stick to underscores
        print(f'now is {datetime.now().strftime("%c")} in UTC')
        print(f'code thinks it is {fileData[1].strftime("%c")}')
        async for message in botChannel.history(around=fileData[1]):
            if len(message.attachments) == 1:
                print("one attachment")
                print(pieceNames)
                print(message.attachments[0].filename)
                if message.attachments[0].filename in pieceNames:
                    print("has a target name")
                    if not os.path.exists(f'{downloads}/Discord File Pieces'):
                        print("making directory")
                        os.mkdir(f'{downloads}/Discord File Pieces')
                    await message.attachments[0].save(
                        f'{downloads}/Discord File Pieces/{message.attachments[0].filename}')
                    print(f'saved {message.attachments[0].filename}')
        await client.close()

    await client.start('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
    return
