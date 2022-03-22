import os
import discord
from datetime import datetime
import GlobalVars
from GlobalVars import *


async def query():
    client = discord.Client()
    masterID = 937444289208778782

    @client.event
    async def on_ready():
        botChannel = await client.fetch_channel(botChannelID)
        await botChannel.send('$downloadList')

    @client.event
    async def on_message(message):
        isMaster = message.author.id == masterID
        if isMaster:  # then it must be the downloadList
            try:
                downloadChoices = message.content
                GlobalVars.fileList = json.loads(downloadChoices)
                with open(currentChoicesPath, 'w') as json_file:
                    json.dump(fileList, json_file, indent=0)
            except Exception as e:
                await message.channel.send(f'Download list query failed because: \n```python\n{str(e)}```')
            await client.close()

    await client.start('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
    return


async def download(fileName):
    client = discord.Client()
    filePieceFolder = f'{downloadsFolder}/Discord File Pieces'
    masterID = 937444289208778782

    @client.event
    async def on_ready():
        try:
            botChannel = await client.fetch_channel(botChannelID)
            await botChannel.send("It's downloadin' time!")
            targetFile = [i for i in GlobalVars.fileList if i['fileName'] == fileName][0]
            message_ids = targetFile['messageIDs']
            fileNum = len(message_ids)
            progress = 0
            for id in message_ids:
                this_message = await botChannel.fetch_message(id)
                if not os.path.exists(filePieceFolder):
                    os.mkdir(filePieceFolder)
                await this_message.attachments[0].save(
                    f'{filePieceFolder}/{this_message.attachments[0].filename}')
                await botChannel.send(f'{fileName} {round(progress / fileNum)}% Downloaded')
            await botChannel.send(f'Downloaded {fileName}')

        except Exception as e:
            await botChannel.send(f'DOWNLOAD FAILED! It has been stopped. Why did it fail? \n```python\n{str(e)}```')

        await client.close()

    await client.start('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
    filePieces = os.listdir(filePieceFolder)
    filePieces.sort()
    realFileName = filePieces[0][:filePieces[0].index('_piece')]
    fileBytes = b''
    for piece in filePieces:
        piecePath = f'{filePieceFolder}/{piece}'
        with open(piecePath, 'rb') as txt:
            fileBytes += txt.read()
            os.rename(piecePath,
                      f'{homeDir}/.Trash/{piece}')
    with open(f'{downloadsFolder}/{realFileName}', 'wb') as writer:
        writer.write(fileBytes)
    # TODO: You know macs don't like modifying Downloads or probably trash from apps, you'll need to find how to do that
    # the user is gonna have to give it Files and Folders permission on newer macs (or full disk access)
    return
