from datetime import datetime

import discord
from GlobalVars import *
from SplitFile import SplitFile


async def upload(filePath):
    client = discord.Client()

    @client.event
    async def on_ready():
        try:
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
            file.set_message_ids(messageIDs)
            uploadData = {
                "fileName": file.name,
                "uploadDate": datetime.now().strftime("%c"),
                "messageIDs": file.messageIDs
            }
            await botChannel.send(f'successfully uploaded:{json.dumps(uploadData)}')
        except Exception as e:
            await botChannel.send(f'UPLOAD FAILED! Error message: \n```python\n{str(e)}```')
        await client.close()

    await client.start('OTI2NjE1OTIyOTA5Nzc3OTgw.Yc-QUw.AjoWXPgpw2HsrwEPTEaJcs2F8q8')
