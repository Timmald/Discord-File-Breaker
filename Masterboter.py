import time
import discord
import json

client = discord.Client()
botChannels = []
fileList = []
channelTranslator = {
    746803793408163898: "Nick's",
    939234547906777139: "Test"
}


@client.event
async def on_ready():
    global botChannels
    global fileList
    botChannels = (await client.fetch_channel(746803793408163898), await client.fetch_channel(939234547906777139))
    with open('filePieces.json', 'r') as json_file:
        fileList = json.load(json_file)
    print("we a'runnin!")


@client.event
async def on_message(message):
    global botChannels
    global fileList
    if message.channel in botChannels and message.author.bot and message.content.startswith('$downloadList'):
        with open('filePieces.json', 'r') as json_file:
            filePieces = json.load(json_file)
            DownloadList = filePieces[channelTranslator[message.channel.id]]
        if len(DownloadList) > 10:
            downloadable = DownloadList[len(DownloadList) - 10:]
        else:
            downloadable = DownloadList
        await message.channel.send(json.dumps(downloadable, indent=0).replace('\'', '\"'))
    elif message.channel in botChannels and message.author.id == 926615922909777980 and len(
            message.attachments) == 0 and message.content.startswith('successfully uploaded'):
        uploadData = message.content.split('successfully uploaded:')[1]
        uploadData = json.loads(uploadData)
        fileList[channelTranslator[message.channel.id]].append(uploadData)
        print("altered fileList")
        time.sleep(1)
        print("naptime!")
        with open('filePieces.json', 'w') as json_file:
            json.dump(fileList, json_file, indent=0)
            print('wrote to json')


client.run('OTM3NDQ0Mjg5MjA4Nzc4Nzgy.Yfb1Bw.ch8l2TGIJWvu_4z5MV1WP0owToo')
