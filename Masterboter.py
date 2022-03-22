import discord
import json
import sqlite3


def get_db_connection():
    return sqlite3.connect('filePieces.sqlite')


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
    print("we a'runnin!")


@client.event
async def on_message(message):
    global botChannels
    global fileList
    if message.channel in botChannels and message.author.bot and message.content.startswith('$downloadList'):
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        DownloadList = conn.execute(
            f'SELECT * FROM File_Pieces WHERE server_name = \'{channelTranslator[message.channel.id]}\'').fetchall()
        if len(DownloadList) > 10:
            downloadable = DownloadList[len(DownloadList) - 10:]
        else:
            downloadable = DownloadList
        # get this list of rows into a meaningful form
        downloadData = []
        for file in downloadable:
            messageIDs = conn.execute('SELECT message_id FROM Message_ids WHERE file_id = :file_id',
                                      {"file_id": file['id']}).fetchall()
            messageIDs = [i['message_id'] for i in messageIDs]
            fileDict = {
                "fileName": file['file_name'],
                "uploadDate": file['upload_time'],
                "messageIDs": messageIDs
            }
            downloadData.append(fileDict)
        await message.channel.send(json.dumps(downloadData, indent=0).replace('\'', '\"'))
        conn.close()
    elif message.channel in botChannels and message.author.id == 926615922909777980 and len(
            message.attachments) == 0 and message.content.startswith('successfully uploaded'):
        uploadData = message.content.split('successfully uploaded:')[1]
        uploadData = json.loads(uploadData)
        name, date, messageIDs = uploadData["fileName"], uploadData["uploadDate"], uploadData["messageIDs"]
        serverName = channelTranslator[message.channel.id]
        conn = get_db_connection()
        conn.row_factory = sqlite3.Row
        conn.execute('INSERT INTO File_Pieces (file_name, upload_time, server_name) VALUES (?, ?, ?)',
                     (name, date, serverName))
        conn.commit()
        current_id = conn.execute('SELECT id FROM File_Pieces ORDER BY id DESC').fetchone()["id"]
        for id in messageIDs:
            conn.execute('INSERT INTO Message_ids (message_id, file_id) VALUES (?, ?)', (id, current_id))
        conn.commit()
        conn.close()


client.run('OTM3NDQ0Mjg5MjA4Nzc4Nzgy.Yfb1Bw.ch8l2TGIJWvu_4z5MV1WP0owToo')
