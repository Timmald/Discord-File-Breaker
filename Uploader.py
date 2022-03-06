import discord
from GlobalVars import *
from SplitFile import SplitFile


async def uploader(filePath):
    client = discord.Client()

    @client.event
    async def on_ready():
        botChannel = await client.fetch_channel(botChannelID)
        await botChannel.send("This confirms that uploader is running")
        file = SplitFile(filePath)
        for name in file.chunkNames:
            fileObj = discord.File(
                open(f'{appSupportFolder}/filePieces/{name}', 'rb'),
                filename=name)
            await botChannel.send(file=fileObj)
        print("sent file")
        await botChannel.send(f'successfully uploaded:{file.fullName}')
        # TODO: Include the message IDs with each piece so that the masterbot can more easily access stuff and speed up downloads soooo much
        await client.close()

    await client.start('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
