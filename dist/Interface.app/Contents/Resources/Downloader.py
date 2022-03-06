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
            downloadChoices = message.content
            GlobalVars.fileList = json.loads(downloadChoices)
            with open(currentChoicesPath, 'w') as json_file:
                json.dump(fileList, json_file, indent=0)
            await client.close()

    await client.start('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
    return


async def download(fileName, pieceNum):
    client = discord.Client()
    filePieceFolder = f'{downloadsFolder}/Discord File Pieces'

    @client.event
    async def on_ready():
        print('yo')
        botChannel = await client.fetch_channel(botChannelID)
        fileData = fileName.split(';_Uploaded_at_')
        fileData[1] = datetime.strptime(fileData[1].replace('_', ' '), '%c')
        pieceNames = [f'{fileData[0]} piece {i}.txt'.replace(' ', '_') for i in range(1, pieceNum + 1)]
        # oh how I wish we could stick to underscores
        async for message in botChannel.history(around=fileData[1]):
            if len(message.attachments) == 1:
                if message.attachments[0].filename in pieceNames:
                    if not os.path.exists(filePieceFolder):
                        os.mkdir(filePieceFolder)
                    await message.attachments[0].save(
                        f'{filePieceFolder}/{message.attachments[0].filename}')
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
    return
