import discord
from GlobalVars import *
from SplitFile import SplitFile


async def upload(filePath):
    client = discord.Client()

    @client.event
    async def on_ready():
        botChannel = await client.fetch_channel(botChannelID)
        await botChannel.send("This confirms that uploader is running")
        file = SplitFile(filePath)
        messageIDs = []
        for name in file.chunkNames:
            fileObj = discord.File(
                open(f'{appSupportFolder}/filePieces/{name}', 'rb'),
                filename=name)
            message = await botChannel.send(file=fileObj)
            messageIDs.append(message.id)
        print("sent file")
        file.set_message_ids(messageIDs)
        await botChannel.send(f'successfully uploaded:{file.fullName()}')
        await client.close()

    await client.start('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
